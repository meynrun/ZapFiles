import ctypes
import hashlib
import json
import os
from logging import error

import colorama as clr
from env import TITLE

from locale import getlocale, windows_locale

clr.init()

if os.name == "nt":
    windll = ctypes.windll.kernel32
    locale = windows_locale[ windll.GetUserDefaultUILanguage() ]
    windll.SetConsoleTitleW("⚡ZapFiles")

else:
    locale = getlocale()[0]

# colors
info_color = clr.Fore.LIGHTBLUE_EX
warn_color = clr.Fore.LIGHTYELLOW_EX
error_color = clr.Fore.LIGHTRED_EX
success_color = clr.Fore.LIGHTGREEN_EX
reset = clr.Style.RESET_ALL


def load_lang(lang_code: str) -> dict:
    """
    Loads language dictionary.

    Args:
        lang_code (str): language code ("en" or "ru")

    Returns:
        Dict: language dictionary
    """
    with open(f"lang/{lang_code}.json", "r", encoding="utf-8") as f:
        return json.load(f)


try:
    if locale == "ru_RU":
        lang = load_lang("ru")
    else:
        lang = load_lang("en")
except FileNotFoundError:
    error("❌ Localization file not found. Fallback to English.")

    try:
        lang = load_lang("en")
    except FileNotFoundError:
        error("❌ Localization file not found.")
        input("Press Enter to exit...")
        exit(1)


def get_file_hash(file_path: str, algorithm: str = 'sha256') -> str:
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


def title() -> None:
    """
    Prints title.

    Returns:
        None
    """
    print(TITLE)


def update() -> None:
    """
    Prints update message.

    Returns:
        None
    """
    print(clr.Fore.LIGHTGREEN_EX + lang["main.info.updateDescription"] + clr.Fore.RESET)


def clear_console() -> None:
    """
    Clears terminal screen.
    
    Returns:
        None
    """
    print('\x1b[2J\x1b[0;0H')


def info(msg) -> None:
    """
    Prints message with info color.

    Args:
        msg (str): message to print
    
    Returns:
        None
    """
    print(f"{info_color}{msg}{reset}")


def warn(msg) -> None:
    """
    Prints message with warn color.

    Args:
        msg (str): message to print
    
    Returns:
        None
    """
    print(f"{warn_color}{msg}{reset}")


def error(msg) -> None:
    """
    Prints message with error color.

    Args:
        msg (str): message to print
    
    Returns:
        None
    """
    print(f"{error_color}{msg}{reset}")


def success(msg) -> None:
    """
    Prints message with success color.

    Args:
        msg (str): message to print
    
    Returns:
        None
    """
    print(f"{success_color}{msg}{reset}")
