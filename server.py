import asyncio
from asyncio import StreamReader, StreamWriter

import requests
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

from typing import Optional


server_config = PrettyTable([lang["server.config.ip"], lang["server.config.port"], lang["server.config.filename"]])


def get_public_ip() -> Optional[str]:
    """
    Gets public IP address.

    Returns:
        str: public IP address
    """
    info(lang["server.info.gettingIp"])

    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=3)

        if response.status_code == 200:
            data = response.content.decode("utf-8")
            ip_info = json.loads(data)
            return ip_info.get("ip")
        else:
            error(lang["universal.error"].format(str(response.status_code) + ", " + response.reason))
            return None

    except requests.exceptions.ConnectTimeout:
        error(lang["update.error.connectionTimedOut"])
        return None

    except requests.exceptions.ConnectionError:
        error(lang["update.error.connectionError"])
        return None


async def handle_client(reader: StreamReader, writer: StreamWriter, filepath: str) -> None:
    """
    Handles client connection.

    Args:
        reader (StreamReader): asyncio StreamReader
        writer (StreamWriter): asyncio StreamWriter
        filepath (str): path to file to send

    Returns:
        None
    """
    try:
        # Getting IP and port of client
        client_ip, client_port = writer.get_extra_info('peername')
        info(lang["server.info.peername"].format(client_ip, client_port))

        # Getting public key
        public_pem = await reader.read(450)
        public_key = serialization.load_pem_public_key(public_pem, backend=default_backend())

        # Генерация симметричного AES-ключа
        aes_key = os.urandom(32)

        # Encrypting AES key by public RSA key
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )

        # Sending encrypted AES key to client
        writer.write(encrypted_aes_key)
        await writer.drain()

        # Sending file size to client
        file_size = os.path.getsize(filepath)
        writer.write(file_size.to_bytes(8, "big"))
        await writer.drain()

        # Encryption and transferring file by chunks
        aes_cipher = Cipher(algorithms.AES(aes_key), modes.CTR(b'0' * 16), backend=default_backend())
        encryptor = aes_cipher.encryptor()

        with tqdm(total=file_size, unit="B", unit_scale=True, desc=os.path.basename(filepath)) as progress_bar:
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
    except ConnectionResetError:
        error(lang["server.error.connectionReset"])
    except ConnectionAbortedError:
        error(lang["server.error.connectionAborted"])
    except ConnectionRefusedError:
        error(lang["server.error.connectionRefused"])
    except Exception as e:
        error(lang["server.error.errorHandlingClient"].format(e))
    finally:
        # Closing streams
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass


async def server() -> None:
    """
    Sets up and starts the server

    Returns:
        None
    """
    # Checking for server_files directory
    server_files_dir = 'server_files'
    if not os.path.exists(server_files_dir):
        warn(lang["server.warn.serverFilesDirNotFound"].format(server_files_dir))
        os.makedirs(server_files_dir)
        success(lang["server.info.directoryCreated"])

    # Setting up server
    warn(lang["server.guide.filesMustBeIn"].format(server_files_dir))
    host_to = "local" if input(lang["server.input.networkType"]) == "2" else "public"

    key_ip = get_public_ip() if host_to == "public" else input(lang["server.input.localIp"])

    if not key_ip:
        error(lang["server.error.publicIpNotFound"])
        return


    # Input filename
    while True:
        files = os.listdir(server_files_dir)

        if len(files) == 0:
            error(lang["server.error.noFiles"])

        print(lang["server.info.filename"])
        for i, file in enumerate(files):
            print(f"    {i + 1}. {file}")

        filename = input(lang["server.input.filename"]) or "1"  # Default to the first file if no input is provided

        if filename == "refresh":
            continue

        try:
            filename = int(filename)
            if 1 <= filename <= len(files):
                filename = files[filename - 1]
            else:
                error(lang["server.error.invalidFilename"])  # Invalid number input
                continue
        except ValueError:
            error(lang["server.error.invalidFilename"])  # Not a number input
            continue

        filepath = f"{server_files_dir}/{filename}"
        if not os.path.exists(filepath):
            error(lang["universal.error.fileNotFound"])
            continue
        else:
            break

    # Input port
    port = int(input(lang["server.input.port"]) or 8888)

    # Starting server
    server_args = partial(handle_client, filepath=filepath)
    host = await asyncio.start_server(server_args, "0.0.0.0", port)

    clear_console()
    title()

    # Printing server information
    server_config.add_row([key_ip, port, filename])
    print(server_config)

    # Generating server key
    server_key = "{}:{}:{}:{}".format(key_ip, port, filename, get_file_hash(filepath))
    success(lang["server.info.serverKey"].format(server_key))

    async with host:
        info(lang["server.info.running"])
        await host.serve_forever()

if __name__ == '__main__':
    asyncio.run(server())
    input(lang["main.enterToExit"])
