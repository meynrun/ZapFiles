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

from shared.file_hash import get_file_hash
from shared.localization import lang
from cli import title, info, warn, err, success, clear_console, color, ColorEnum
import os

from typing import Optional


server_config = PrettyTable([lang.get_string("server.config.ip"), lang.get_string("server.config.port"), lang.get_string("server.config.filename")])


def get_public_ip() -> Optional[str]:
    """
    Gets public IP address.

    Returns:
        str: public IP address
    """
    info(lang.get_string("server.info.gettingIp"))

    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=3)

        if response.status_code == 200:
            data = response.content.decode("utf-8")
            ip_info = json.loads(data)
            return ip_info.get("ip")
        else:
            err(lang.get_string("universal.err").format(str(response.status_code) + ", " + response.reason))
            return None

    except requests.exceptions.ConnectTimeout:
        err(lang.get_string("update.error.connectionTimedOut"))
        return None

    except requests.exceptions.ConnectionError:
        err(lang.get_string("update.error.connectionError"))
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
        info(lang.get_string("server.info.peername").format(client_ip, client_port))

        # Getting public key
        public_key = serialization.load_pem_public_key(await reader.read(450), backend=default_backend())

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
        success(lang.get_string("server.info.fileSent"))
    except ConnectionResetError:
        err(lang.get_string("server.error.connectionReset"))
    except ConnectionAbortedError:
        err(lang.get_string("server.error.connectionAborted"))
    except ConnectionRefusedError:
        err(lang.get_string("server.error.connectionRefused"))
    except Exception as e:
        err(lang.get_string("server.error.errorHandlingClient").format(e))
    finally:
        # Closing streams
        try:
            writer.close()
            await writer.wait_closed()
        finally:
            return


async def server() -> None:
    """
    Sets up and starts the server

    Returns:
        None
    """
    try:
        # Checking for server_files directory
        server_files_dir = 'server_files'
        if not os.path.exists(server_files_dir):
            warn(lang.get_string("server.warn.serverFilesDirNotFound").format(server_files_dir))
            os.makedirs(server_files_dir)
            success(lang.get_string("server.info.directoryCreated"))

        # Setting up server
        warn(lang.get_string("server.guide.filesMustBeIn").format(server_files_dir))

        host_to = "local" if input(color(lang.get_string("server.input.networkType"), ColorEnum.WARN, ColorEnum.SUCCESS)) == "2" else "public"

        key_ip = get_public_ip() if host_to == "public" else input(color(lang.get_string("server.input.localIp"), ColorEnum.WARN, ColorEnum.SUCCESS))

        if not key_ip:
            err(lang.get_string("server.error.publicIpNotFound"))
            return

        filepath: str = ""
        # Input filename
        while True:
            files = os.listdir(server_files_dir)

            if len(files) == 0:
                err(lang.get_string("server.error.noFiles"))

            print(lang.get_string("server.info.filename"))
            for i, file in enumerate(files):
                print(f"    {i + 1}. {file}")

            filename = input(color(lang.get_string("server.input.filename"), ColorEnum.WARN, ColorEnum.SUCCESS)) or "1"  # Default to the first file if no input is provided

            if filename == "refresh":
                continue

            try:
                filename = int(filename)
                if 1 <= filename <= len(files):
                    filename = files[filename - 1]
                else:
                    err(lang.get_string("server.error.invalidFilename"))  # Invalid number input
                    continue
            except ValueError:
                err(lang.get_string("server.error.invalidFilename"))  # Not a number input
                continue

            filepath = f"{server_files_dir}/{filename}"
            if not os.path.exists(filepath):
                err(lang.get_string("universal.error.fileNotFound"))
                continue
            else:
                break

        # Input port
        port = int(input(color(lang.get_string("server.input.port"), ColorEnum.WARN, ColorEnum.SUCCESS)) or 8888)

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
        success(lang.get_string("server.info.serverKey").format(server_key))

        async with host:
            info(lang.get_string("server.info.running"))
            await host.serve_forever()
    except EOFError:
        return

if __name__ == '__main__':
    asyncio.run(server())
    input(lang.get_string("main.enterToExit"))
