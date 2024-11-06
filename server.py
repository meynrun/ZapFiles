import asyncio
import http.client
import json

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from functools import partial
from prettytable import PrettyTable
from tqdm import tqdm

from shared import lang
from shared import info, warn, error, success, clear_console, get_file_hash, title
import os


server_config = PrettyTable(['🖥️ IP', '🔌 Port', '📄 Filename'])


def get_public_ip():
    conn = http.client.HTTPSConnection("api.ipify.org")
    conn.request("GET", "/?format=json")

    response = conn.getresponse()
    if response.status == 200:
        data = response.read().decode("utf-8")
        ip_info = json.loads(data)
        return ip_info.get("ip")
    else:
        print("Error: {} {}".format(response.status, response.reason))
    conn.close()


async def handle_client(reader, writer, filepath):
    try:
        # Получаем IP-адрес и порт клиента
        client_ip, client_port = writer.get_extra_info('peername')
        info(lang["server.info.peername"].format(client_ip, client_port))

        # Получение публичного ключа клиента
        public_pem = await reader.read(450)
        public_key = serialization.load_pem_public_key(public_pem, backend=default_backend())

        # Генерация симметричного AES-ключа
        aes_key = os.urandom(32)

        # Шифрование AES-ключа с помощью публичного ключа клиента
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )

        # Отправка зашифрованного AES-ключа клиенту
        writer.write(encrypted_aes_key)
        await writer.drain()

        # Отправка размера файла клиенту
        file_size = os.path.getsize(filepath)
        writer.write(file_size.to_bytes(8, "big"))
        await writer.drain()

        # Шифрование и передача файла по частям
        aes_cipher = Cipher(algorithms.AES(aes_key), modes.CTR(b'0' * 16), backend=default_backend())
        encryptor = aes_cipher.encryptor()

        with tqdm(total=file_size, unit="B", unit_scale=True, desc=filepath) as progress_bar:
            with open(filepath, "rb") as f:
                while True:
                    file_data = f.read(4096)
                    if not file_data:
                        break
                    encrypted_file_data = encryptor.update(file_data)
                    writer.write(encrypted_file_data)
                    await writer.drain()
                    progress_bar.update(len(file_data))

        writer.write(encryptor.finalize())
        await writer.drain()
        success(lang["server.info.fileSent"])
    except Exception as e:
        error(lang["server.error.errorHandlingClient"].format(e))
    finally:
        writer.close()
        await writer.wait_closed()


async def server():
    # Проверка наличия каталога с файлами
    server_files_dir = './server_files'
    if not os.path.exists(server_files_dir):
        warn(lang["server.error.serverFilesDirNotFound"].format(server_files_dir))
        os.makedirs(server_files_dir)
        success(lang["server.info.directoryCreated"])

    # Настройка сервера
    print(lang["server.guide.filesMustBeIn"].format(server_files_dir))
    host_to = "0.0.0.0"\
        if input(lang["server.input.networkType"]) == "1"\
        else "localhost"

    key_ip = get_public_ip() if host_to == "0.0.0.0" else input(lang["server.input.localIp"])

    # Ввод имени файла
    while True:
        filename = input(lang["server.input.filename"]) or os.urandom(1).hex()
        filepath = f"{server_files_dir}/{filename}"
        if not os.path.exists(filepath):
            error(lang["server.error.fileNotFound"])
        else:
            break

    port = int(input(lang["server.input.port"]) or 8888)

    # Запуск сервера
    server_args = partial(handle_client, filepath=filepath)
    host = await asyncio.start_server(server_args, host_to, port)

    clear_console()
    title()

    # Добавление информации о сервере в таблицу
    server_config.add_row([host_to, port, filename])

    print(server_config)

    # Генерация публичного ключа сервера
    server_key = "{}:{}:{}:{}".format(key_ip, port, filename, get_file_hash(filepath))
    success(lang["server.info.serverKey"].format(server_key))

    async with host:
        info(lang["server.info.running"])
        await host.serve_forever()

if __name__ == '__main__':
    asyncio.run(server())
    input(lang["main.enterToExit"])
