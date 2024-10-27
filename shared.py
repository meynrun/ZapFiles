import hashlib
import colorama as clr


info_color = clr.Fore.LIGHTBLUE_EX
warn_color = clr.Fore.LIGHTYELLOW_EX
error_color = clr.Fore.LIGHTRED_EX
success_color = clr.Fore.LIGHTGREEN_EX
reset = clr.Style.RESET_ALL


def get_file_hash(file_path, algorithm='sha256'):
    # Выбор алгоритма хеширования
    hash_func = hashlib.new(algorithm)

    # Чтение файла по блокам, чтобы избежать загрузки больших файлов в память
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            hash_func.update(block)

    # Возвращаем хеш-сумму в виде строки
    return hash_func.hexdigest()


def clear_console():
    print('\x1b[2J\x1b[0;0H')


def info(msg):
    print(f"{info_color}{msg}{reset}")


def warn(msg):
    print(f"{warn_color}{msg}{reset}")


def error(msg):
    print(f"{error_color}{msg}{reset}")


def success(msg):
    print(f"{success_color}{msg}{reset}")
