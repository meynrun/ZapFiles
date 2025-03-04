import asyncio
from asyncio import StreamReader, StreamWriter

from experiments.experiments_config import enabled_experiments

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes, CipherContext
from cryptography.hazmat.backends import default_backend

from shared import info, warn, error, success, clear_console, get_file_hash, lang, title
import os
from tqdm import tqdm
from getpass import getuser


def get_download_path(filename: str) -> str:
    """
    Returns path to downloads directory.

    Args:
        filename (str): name of file

    Returns:
        str: path to downloads directory
    """
    if "file_classification" in enabled_experiments:
        if os.name == "nt":
            return f"C:/Users/{getuser()}/Downloads/ZapFiles Downloads/{os.path.splitext(filename)[1]}/{filename}"
        else:
            return f"./downloaded_files/{os.path.splitext(filename)[1]}/{filename}"
    else:
        if os.name == "nt":
            return f"C:/Users/{getuser()}/Downloads/ZapFiles Downloads/{filename}"
        else:
            return f"./downloaded_files{filename}"


async def send_public_key(writer: StreamWriter, public_key: rsa.RSAPublicKey) -> None:
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
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    writer.write(public_pem)
    await writer.drain()


async def receive_encrypted_key(reader: StreamReader) -> bytes:
    """
    Receives encrypted AES key from server.

    Args:
        reader (StreamReader): asyncio StreamReader

    Returns:
        bytes: encrypted AES key
    """
    return await reader.read(256)


def create_aes_cipher(aes_key: bytes) -> Cipher:
    """
    Creates AES cipher.

    Args:
        aes_key (bytes): AES key

    Returns:
        Cipher: AES cipher
    """
    return Cipher(algorithms.AES(aes_key), modes.CTR(b'0' * 16), backend=default_backend())


async def save_decrypted_file(reader: StreamReader, file_path: str, decryptor: CipherContext, file_size: int) -> None:
    """
    Saves decrypted file.

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

    # Creating progressbar with total size of file
    with tqdm(total=file_size, unit="B", unit_scale=True, desc=os.path.basename(file_path)) as progress_bar:
        with open(file_path, "wb") as f:
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                f.write(decryptor.update(data))
                progress_bar.update(len(data))

            f.write(decryptor.finalize())


async def download_file(ip: str, port: int, filename: str, file_hash: str) -> None:
    """
    Downloads file from server.

    Args:
        ip (str): IP address of server
        port (int): port of server
        filename (str): name of file to download
        file_hash (str): hash of file to download

    Returns:
        None
    """
    # Generating RSA keys
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Connecting to server
    reader, writer = await asyncio.open_connection(ip, port)
    await send_public_key(writer, public_key)

    # Getting encrypted AES key from server
    encrypted_aes_key = await receive_encrypted_key(reader)

    try:
        # Decrypting AES key
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
    except ValueError:
        error(lang["client.error.invalidEncryptionKey"])
        return

    # Getting total size of file from server
    file_size_data = await reader.read(8)
    file_size = int.from_bytes(file_size_data, "big")

    # Creating decryptor
    decryptor = create_aes_cipher(aes_key).decryptor()

    # Creating file path
    file_path = get_download_path(filename)

    # Saving file
    await save_decrypted_file(reader, file_path, decryptor, file_size)

    success(lang["client.info.fileReceived"])
    validate_file(file_path, file_hash)

    writer.close()
    await writer.wait_closed()


def validate_file(file_path: str, file_hash: str) -> None:
    """
    Validates file hash.

    Args:
        file_path (str): path to file to validate
        file_hash (str): file hash

    Returns:
        None
    """
    # Checking file hash
    info(lang["client.hash.checking"])
    if get_file_hash(file_path) == file_hash:
        success(lang["client.hash.correct"])
    else:
        error(lang["client.hash.incorrect"])
        handle_file_deletion(file_path)


def handle_file_deletion(file_path: str) -> None:
    """
    Handles file deletion.

    Args:
        file_path (str): path to file to delete

    Returns:
        None
    """
    try:
        if os.path.exists(file_path):
            if input(lang["client.choose.delete"]).strip().lower() == "y":
                os.remove(file_path)
                success(lang["client.info.fileDeleted"])
            else:
                success(lang["client.info.fileSaved"])
                return
    except PermissionError:
        error(lang["client.error.filePermissionError"])
        return
    except FileNotFoundError:
        return
    except EOFError:
        return
    except Exception as e:
        error(str(e))
        return


async def client() -> None:
    """
    Main client function.

    Returns:
        None
    """
    clear_console()
    title()

    try:
        server_key = input(lang["client.input.key"])
    except EOFError:
        return

    # Parsing server key
    try:
        ip, port, filename, file_hash = server_key.split(":")
        port = int(port)  # converting port to int
    except ValueError:
        error(lang["client.error.invalidKey"])
        return

    # Checking if client already have that file
    file_path = get_download_path(filename)
    if os.path.exists(file_path) and get_file_hash(file_path) == file_hash:
        warn(lang["client.warning.fileAlreadyExists"])
        handle_file_deletion(file_path)

    elif os.path.exists(file_path):
        warn(lang["client.warning.fileWithSameNameExists"])
        handle_file_deletion(file_path)

    await download_file(ip, port, filename, file_hash)


if __name__ == '__main__':
    asyncio.run(client())
    input(lang["main.enterToExit"])

