import hashlib
from os import PathLike


def get_file_hash(file_path: PathLike[str], algorithm: str = "sha256") -> str:
    """
    Returns file hash.
    By default, uses sha256.

    Args:
        file_path (str): path to file to hash
        algorithm (str): hash algorithm (default: sha256)

    Returns:
        Str: file hash
    """
    hash_func = hashlib.new(algorithm)

    # Reading file by chunks
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            hash_func.update(block)

    return hash_func.hexdigest()
