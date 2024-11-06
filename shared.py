import hashlib
import json

import colorama as clr
import env

from locale import getlocale

clr.init()

locale = getlocale()[0]
ru_locales = [
    # Windows 
    "Russian_Russia",
    "Russian_Belarus",
    "Russian_Kazakhstan",
    "Russian_Ukraine",
    "Russian_Kyrgyzstan",
    "Russian_Tajikistan",
    "Russian_Armenia",

    # macOS и Linux 
    "ru_RU",
    "ru_BY",
    "ru_KZ",
    "ru_UA",
    "ru_KG",
    "ru_TJ",
    "ru_AM",
    "ru_RU.UTF-8",
    "ru_BY.UTF-8",
    "ru_KZ.UTF-8",
    "ru_UA.UTF-8",
    "ru_KG.UTF-8",
    "ru_TJ.UTF-8",
    "ru_AM.UTF-8"
]


info_color = clr.Fore.LIGHTBLUE_EX
warn_color = clr.Fore.LIGHTYELLOW_EX
error_color = clr.Fore.LIGHTRED_EX
success_color = clr.Fore.LIGHTGREEN_EX
reset = clr.Style.RESET_ALL


def load_lang(lang):
    with open(f"lang/{lang}.json", "r", encoding="utf-8") as f:
        return json.load(f)

try:
    if locale in ru_locales:
        lang = load_lang("ru")
    else:
        lang = load_lang("en")
except FileNotFoundError:
    print("Файл локализации не найден. Используется язык по умолчанию.")

    try:
        lang = load_lang("en")
    except FileNotFoundError:
        print("Файл локализации не найден. Выход из программы.")
        exit(1)



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
