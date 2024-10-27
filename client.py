import asyncio
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from shared import info, warn, error, success, clear_console, get_file_hash
import os
from tqdm import tqdm  # Импортируем tqdm для прогресс-бара


async def send_public_key(writer, public_key):
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    writer.write(public_pem)
    await writer.drain()


async def receive_encrypted_key(reader):
    return await reader.read(256)


def create_aes_cipher(aes_key):
    return Cipher(algorithms.AES(aes_key), modes.CTR(b'0' * 16), backend=default_backend())


async def save_decrypted_file(reader, file_path, decryptor, file_size):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Создаем прогресс-бар на основе общего размера файла
    with tqdm(total=file_size, unit="B", unit_scale=True, desc=file_path) as progress_bar:
        with open(file_path, "wb") as f:
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                f.write(decryptor.update(data))
                progress_bar.update(len(data))  # Обновляем прогресс-бар

            f.write(decryptor.finalize())


async def download_file(ip, port, filename, file_hash):
    # Генерация ключей RSA для клиента
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Подключение к серверу
    reader, writer = await asyncio.open_connection(ip, port)
    await send_public_key(writer, public_key)

    # Получение зашифрованного AES-ключа от сервера
    encrypted_aes_key = await receive_encrypted_key(reader)

    # Расшифровка AES-ключа
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    # Чтение размера файла от сервера
    file_size_data = await reader.read(8)
    file_size = int.from_bytes(file_size_data, "big")

    # Создание объекта AES для расшифровки
    decryptor = create_aes_cipher(aes_key).decryptor()
    file_path = f"./downloaded_files/{filename}"

    # Сохранение расшифрованного файла с прогресс-баром
    await save_decrypted_file(reader, file_path, decryptor, file_size)

    success("✅ File received and decrypted.")
    validate_file(file_path, file_hash)

    writer.close()
    await writer.wait_closed()


def validate_file(file_path, file_hash):
    info("🔍 Checking file hash...")
    if get_file_hash(file_path) == file_hash:
        success("✅ File hash is correct.")
    else:
        error("❌ File hash is incorrect.")
        handle_file_deletion(file_path)


def handle_file_deletion(file_path):
    if os.path.exists(file_path):
        if input("🗑️ Do you want to delete this file? (y/n): ").strip().lower() == "y":
            os.remove(file_path)
            success("🔥 File deleted.")
        else:
            success("💾 File saved.")
            return


async def client():
    server_key = input("🔑 Enter server key: ")

    # Разбор ключа сервера
    try:
        ip, port, filename, file_hash = server_key.split(":")
        port = int(port)  # Преобразуем порт в int
    except ValueError:
        error("❌ Invalid server key format. Please use 'ip:port:filename:file_hash'")
        return

    # Проверка на наличие файла
    file_path = f"./downloaded_files/{filename}"
    if os.path.exists(file_path) and get_file_hash(file_path) == file_hash:
        warn("⚠️ File already exists.")
        handle_file_deletion(file_path)

    elif os.path.exists(file_path):
        warn("⚠️ File with this name already exists, but with a different hash.")
        handle_file_deletion(file_path)

    await download_file(ip, port, filename, file_hash)


if __name__ == '__main__':
    asyncio.run(client())
    input('\nPress Enter to exit...')

