import ctypes
import hashlib
import json
import os
import re
from logging import error

import colorama as clr
from env import TITLE

from locale import getlocale, windows_locale
from config_file import config

clr.init()

# colors
info_color = clr.Fore.LIGHTBLUE_EX
warn_color = clr.Fore.LIGHTYELLOW_EX
error_color = clr.Fore.LIGHTRED_EX
success_color = clr.Fore.LIGHTGREEN_EX
reset = clr.Style.RESET_ALL


def remove_emojis(text):
    return re.sub(r"[\U0001F000-\U0001FAFF]\s*", "", text)


def load_lang_dict(lang_code: str) -> dict:
    """
    Loads language dictionary.

    Args:
        lang_code (str): language code ("en" or "ru")

    Returns:
        Dict: language dictionary
    """
    with open(f"lang/{lang_code}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_lang() -> tuple[str | None, dict]:
    """
    Loads language code and language dictionary.

    Returns:
        Tuple[str | None, Dict]: language code and language dictionary
    """
    if os.name == "nt":
        windll = ctypes.windll.kernel32
        windll.SetConsoleTitleW("⚡ZapFiles")

    lang_code = config["language"]

    if lang_code != "auto":
        try:
            lang_code = config["language"]
            lang_dict = load_lang_dict(lang_code)
        except FileNotFoundError:
            error(f"❌ Localization file for {lang_code} not found. Fallback to English.")

            try:
                lang_dict = load_lang_dict("en")
            except FileNotFoundError:
                error("❌ Localization file not found.")
                input("Press Enter to exit...")
                exit(1)
    else:
        if os.name == "nt":
            windll = ctypes.windll.kernel32
            lang_code = windows_locale[windll.GetUserDefaultUILanguage()]
        else:
            lang_code = getlocale()[0]

        try:
            if lang_code == "ru_RU":
                lang_dict = load_lang_dict("ru")
            else:
                lang_dict = load_lang_dict("en")
        except FileNotFoundError:
            error(f"❌ Localization file for {lang_code} not found. Fallback to English.")

            try:
                lang_dict = load_lang_dict("en")
            except FileNotFoundError:
                error("❌ Localization file not found.")
                input("Press Enter to exit...")
                exit(1)

    if not config["enable_emojis"]:
        lang_dict = {key: remove_emojis(value) for key, value in lang_dict.items()}

    return lang_code, lang_dict


locale, lang = load_lang()


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
    if config["clear_mode"] == "ASCII":
        print('\033[H\033[J', end='', flush=True)
    elif config["clear_mode"] == "command":
        os.system("cls" if os.name == "nt" else "clear")
    elif config["clear_mode"] == "ASCII2":
        print('\x1b[2J\x1b[0;0H', end='', flush=True)


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
