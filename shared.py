import hashlib
import json

import colorama as clr
import env


info_color = clr.Fore.LIGHTBLUE_EX
warn_color = clr.Fore.LIGHTYELLOW_EX
error_color = clr.Fore.LIGHTRED_EX
success_color = clr.Fore.LIGHTGREEN_EX
reset = clr.Style.RESET_ALL


def load_lang(lang):
    with open(f"lang/{lang}.json", "r", encoding="utf-8") as f:
        return json.load(f)

lang = load_lang("en_us")


def get_file_hash(file_path, algorithm='sha256'):
    # Выбор алгоритма хеширования
    hash_func = hashlib.new(algorithm)

    # Чтение файла по блокам, чтобы избежать загрузки больших файлов в память
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            hash_func.update(block)

    # Возвращаем хеш-сумму в виде строки
    return hash_func.hexdigest()





def title():
    print(env.TITLE)


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
