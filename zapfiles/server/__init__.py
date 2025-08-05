import asyncio
import json
import os
from asyncio import StreamReader, StreamWriter
from functools import partial
from os import PathLike
from pathlib import Path
from typing import Optional

import questionary
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from prettytable import PrettyTable
from tqdm import tqdm

from zapfiles.cli import (
    title,
    info,
    warn,
    err,
    success,
    clear_console,
    color,
    ColorEnum,
)
from zapfiles.constants import ROOT_DIR
from zapfiles.core.hash import get_file_hash
from zapfiles.core.localization import lang
from zapfiles.core.config.app_configuration import config

server_config = PrettyTable(
    [
        lang.get_string("server.config.ip"),
        lang.get_string("server.config.port"),
        lang.get_string("server.config.filename"),
    ]
)


def assert_rsa_key(key) -> RSAPublicKey:
    if not isinstance(key, RSAPublicKey):
        raise TypeError("Ключ не является RSA-ключом")
    return key


def get_public_ip() -> Optional[str]:
    """
    Gets public IP address.

    Returns:
        str: public IP address
    """
    print(color(lang.get_string("server.info.gettingIp"), ColorEnum.INFO), end=" ")

    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=3)

        if response.status_code == 200:
            data = response.content.decode("utf-8")
            ip = json.loads(data).get("ip")
            print(color(ip, ColorEnum.WARN))
            return ip
        else:
            err(
                lang.get_string("universal.err").format(
                    str(response.status_code) + ", " + response.reason
                )
            )
            return None

    except requests.exceptions.ConnectTimeout:
        err(lang.get_string("update.error.connectionTimedOut"))
        return None

    except requests.exceptions.ConnectionError:
        err(lang.get_string("update.error.connectionError"))
        return None

    except requests.exceptions.ReadTimeout:
        err(lang.get_string("update.error.connectionTimedOut"))
        return None


async def handle_client(
    reader: StreamReader, writer: StreamWriter, filepath: PathLike[str]
) -> None:
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
        client_ip, client_port = writer.get_extra_info("peername")
        info(lang.get_string("server.info.peername").format(client_ip, client_port))

        # Getting public key
        public_key = assert_rsa_key(
            serialization.load_pem_public_key(
                await reader.read(450), backend=default_backend()
            )
        )

        # Генерация симметричного AES-ключа
        aes_key = os.urandom(32)

        # Encrypting AES key by public RSA key
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # Sending encrypted AES key to client
        writer.write(encrypted_aes_key)
        await writer.drain()

        # Sending file size to client
        file_size = os.path.getsize(filepath)
        writer.write(file_size.to_bytes(8, "big"))
        await writer.drain()

        # Encryption and transferring file by chunks
        aes_cipher = Cipher(
            algorithms.AES(aes_key), modes.CTR(b"0" * 16), backend=default_backend()
        )
        encryptor = aes_cipher.encryptor()

        with tqdm(
            total=file_size, unit="B", unit_scale=True, desc=os.path.basename(filepath)
        ) as progress_bar:
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
        server_files_dir = Path(ROOT_DIR) / "server_files"
        if not os.path.exists(server_files_dir):
            warn(
                lang.get_string("server.warn.serverFilesDirNotFound").format(
                    server_files_dir
                )
            )
            os.makedirs(server_files_dir)
            success(lang.get_string("server.info.directoryCreated"))

        # Setting up server
        host_ip = await questionary.select(
            message=lang.get_string("server.input.networkType"),
            choices=[
                {
                    "name": lang.get_string("server.input.networkType.public"),
                    "value": "public",
                },
                {
                    "name": lang.get_string("server.input.networkType.custom"),
                    "value": "custom",
                },
            ],
        ).ask_async()

        key_ip = (
            get_public_ip()
            if host_ip == "public"
            else await questionary.text(
                lang.get_string("server.input.customIp")
            ).ask_async()
        )

        if not key_ip:
            err(lang.get_string("server.error.invalidIp"))
            return

        if config.get_value("enable_tips"):
            info(lang.get_string("server.tip.storageDirectory"))
            info(lang.get_string("server.tip.fileNavigation"))

        while True:
            file_path = await questionary.path(
                message=lang.get_string("server.info.filePath")
            ).ask_async()
            try:
                if Path(file_path).is_file():
                    break
                err(lang.get_string("server.error.fileNotFound").format(file=file_path))
            except TypeError:
                if not file_path:
                    return
                err(lang.get_string("server.error.fileNotFound").format(file=file_path))

        # Input port
        while True:
            port_input = ""
            try:
                port_input = (
                    await questionary.text(
                        lang.get_string("server.input.port")
                    ).ask_async()
                    or 8888
                )
                port = int(port_input)
                if port <= 0 or port > 65535:
                    raise ValueError
            except ValueError:
                err(lang.get_string("server.error.invalidPort").format(port=port_input))
            else:
                break

        # Starting server
        server_args = partial(handle_client, filepath=file_path)
        host = await asyncio.start_server(server_args, "0.0.0.0", port)

        clear_console()
        title()

        filename: str = os.path.basename(file_path)

        # Printing server information
        server_config.add_row([key_ip, port, filename])
        print(server_config)

        file_hash = get_file_hash(file_path)

        # Generating server key
        server_key = "{}:{}:{}:{}".format(key_ip, port, filename, file_hash)
        success(lang.get_string("server.info.serverKey").format(server_key))

        os.makedirs("generated_zapfiles", exist_ok=True)
        with open(
            Path("generated_zapfiles") / f"{filename}.zapfile", "w", encoding="utf-8"
        ) as f:
            zapfile = {
                "host": key_ip,
                "port": port,
                "filename": filename,
                "hash": file_hash,
            }
            f.write(json.dumps(zapfile, indent=4, ensure_ascii=False))
            success(
                lang.get_string("server.info.createdZapfile").format(
                    filename + ".zapfile"
                )
            )

        async with host:
            info(lang.get_string("server.info.running"))
            await host.serve_forever()
    except EOFError:
        return


if __name__ == "__main__":
    asyncio.run(server())
    input(lang.get_string("main.enterToExit"))
