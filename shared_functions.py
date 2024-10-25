import hashlib


def get_file_hash(file_path, algorithm='sha256'):
    # Выбор алгоритма хеширования
    hash_func = hashlib.new(algorithm)

    # Чтение файла по блокам, чтобы избежать загрузки больших файлов в память
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            hash_func.update(block)

    # Возвращаем хеш-сумму в виде строки
    return hash_func.hexdigest()