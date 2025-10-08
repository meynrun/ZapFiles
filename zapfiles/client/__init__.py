import asyncio
import os
from asyncio import StreamReader, StreamWriter
from os import PathLike
from pathlib import Path

import questionary
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes,
    CipherContext,
)
from tqdm import tqdm

from zapfiles.cli import info, warn, err, success, clear_console, title, ColorEnum
from zapfiles.core.config.app_configuration import config
from zapfiles.core.config.experiments_configuration import experiments_config
from zapfiles.core.hash import get_file_hash
from zapfiles.core.localization import lang


def get_download_path(filename: str) -> Path:
    """
    Returns path to downloads directory.

    Args:
        filename (str): name of file

    Returns:
        str: path to downloads directory
    """
    if "file_classification" in experiments_config.get_enabled_experiments():
        return (
            Path(config.get_value("downloads_path"))
            / os.path.splitext(filename)[-1]
            / filename
        )
    else:
        return Path(config.get_value("downloads_path")) / filename


async def send_public_key(writer: StreamWriter, public_key: RSAPublicKey) -> None:
    """
    Sends public key to server.

    Args:
        writer (StreamWriter): asyncio StreamWriter
        public_key (rsa.RSAPublicKey): public RSA key

    Returns:
        None
    """
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    writer.write(public_pem)
    await writer.drain()


def create_aes_cipher(aes_key: bytes, nonce: bytes) -> Cipher:
    """
    Creates AES cipher.

    Args:
        aes_key (bytes): AES key
        nonce (bytes): nonce

    Returns:
        Cipher: AES cipher
    """
    return Cipher(algorithms.AES(aes_key), modes.CTR(nonce), backend=default_backend())


def decrypt_using_private_key(private_key: RSAPrivateKey, data: bytes) -> bytes:
    try:
        return private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except ValueError:
        err(lang.get_string("client.error.failedToDecryptData"))
        return b""


async def download_and_decrypt_file(
    reader: StreamReader, file_path: Path, decryptor: CipherContext, file_size: int
) -> None:
    """
    Downloads file from server.

    Args:
        reader (StreamReader): asyncio StreamReader
        file_path (str): path to save file
        decryptor (CipherContext): decryptor
        file_size (int): size of file

    Returns:
        None
    """
    # Creating directory
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    print(ColorEnum.SUCCESS, end="", flush=True)

    # Creating progressbar with total size of file
    with tqdm(
        total=file_size, unit="B", unit_scale=True, desc=os.path.basename(file_path)
    ) as progress_bar:
        with open(file_path, "wb") as f:
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                f.write(decryptor.update(data))
                progress_bar.update(len(data))

            f.write(decryptor.finalize())


def generate_rsa() -> tuple[RSAPrivateKey, RSAPublicKey]:
    """
    Generates RSA key pair.

    Returns:
        tuple[RSAPrivateKey, RSAPublicKey]: RSA key pair
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


async def connect(ip: str, port: int, filename: str, file_hash: str) -> None:
    """
    Establishes connection to server.

    Args:
        ip (str): IP address of server
        port (int): port of server
        filename (str): name of file to download
        file_hash (str): hash of file to download

    Returns:
        None
    """
    # Generating RSA keys
    private_key, public_key = generate_rsa()

    # Connecting to server
    reader, writer = await asyncio.open_connection(ip, port)
    await send_public_key(writer, public_key)

    # Getting encrypted AES key and nonse from server
    encrypted_aes_key = await reader.read(256)
    encrypted_nonce = await reader.read(256)

    aes_key = decrypt_using_private_key(private_key, encrypted_aes_key)
    nonce = decrypt_using_private_key(private_key, encrypted_nonce)

    if not aes_key or not nonce:
        return

    # Getting total size of file from server
    file_size_data = await reader.read(8)
    file_size = int.from_bytes(file_size_data, "big")

    # Creating decryptor
    decryptor = create_aes_cipher(aes_key, nonce).decryptor()

    # Creating file path
    file_path = get_download_path(filename)

    # Saving file
    await download_and_decrypt_file(reader, file_path, decryptor, file_size)

    success(lang.get_string("client.info.fileReceived"))
    await validate_file(file_path, file_hash)

    writer.close()
    await writer.wait_closed()


async def validate_file(file_path: PathLike[str], file_hash: str) -> None:
    """
    Validates file hash.

    Args:
        file_path (PathLike[str]): path to file to validate
        file_hash (str): file hash

    Returns:
        None
    """
    # Checking file hash
    info(lang.get_string("client.hash.checking"))
    if get_file_hash(file_path) == file_hash:
        success(lang.get_string("client.hash.correct"))
    else:
        err(lang.get_string("client.hash.incorrect"))
        await handle_file_deletion(file_path)


async def handle_file_deletion(file_path: PathLike[str]) -> bool | None:
    """
    Handles file deletion.

    Args:
        file_path (PathLike[str]): path to file to delete

    Returns:
        bool: True if file was deleted
    """
    try:
        if os.path.exists(file_path):
            if await questionary.confirm(
                lang.get_string("client.choose.delete")
            ).ask_async():
                os.remove(file_path)
                success(lang.get_string("client.info.fileDeleted"))
                return True
            else:
                success(lang.get_string("client.info.fileSaved"))
                return False
    except PermissionError:
        err(lang.get_string("client.error.filePermissionError"))
        return False
    except FileNotFoundError:
        return False
    except EOFError:
        return False
    except Exception as e:
        err(str(e))
        return False


async def client() -> None:
    """
    Main client function.

    Returns:
        None
    """
    clear_console()
    title()

    server_key = await questionary.text(lang.get_string("client.input.key")).ask_async()
    if not server_key:
        return

    # Parsing server key
    try:
        ip, port, filename, file_hash = server_key.split(":")
        port = int(port)  # converting port to int
    except ValueError:
        err(lang.get_string("client.error.invalidKey"))
        return

    # Checking if client already have that file
    file_path = get_download_path(filename)
    if os.path.exists(file_path) and get_file_hash(file_path) == file_hash:
        warn(lang.get_string("client.warning.fileAlreadyExists"))
        if not await handle_file_deletion(file_path):
            return  # if file was not deleted don't download it again

    elif os.path.exists(file_path):
        warn(lang.get_string("client.warning.fileWithSameNameExists"))
        if not await handle_file_deletion(file_path):
            return

    await connect(ip, port, filename, file_hash)


if __name__ == "__main__":
    asyncio.run(client())
    input(lang.get_string("main.enterToExit"))
