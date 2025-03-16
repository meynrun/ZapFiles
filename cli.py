import os

import colorama as clr
from colorama import Fore

from config.app_configuration import config
from env import VERSION

clr.init()

# colors
info_color = clr.Fore.LIGHTBLUE_EX
warn_color = clr.Fore.LIGHTYELLOW_EX
error_color = clr.Fore.LIGHTRED_EX
success_color = clr.Fore.LIGHTGREEN_EX
reset = clr.Style.RESET_ALL


def title() -> None:
    """
    Prints title.

    Returns:
        None
    """
    if config.get_value("enable_emojis"):
        title_text = f"""{Fore.LIGHTYELLOW_EX}ZapFiles {Fore.LIGHTWHITE_EX}{VERSION}
{Fore.LIGHTYELLOW_EX}Made with 💖 by {Fore.LIGHTBLUE_EX}Meynrun
    """
    else:
        title_text = f"""{Fore.LIGHTYELLOW_EX}ZapFiles {Fore.LIGHTWHITE_EX}{VERSION}
{Fore.LIGHTYELLOW_EX}Made with love by {Fore.LIGHTBLUE_EX}Meynrun
    """
    print(title_text)


def clear_console() -> None:
    """
    Clears terminal screen.

    Returns:
        None
    """
    if config.get_value("clear_mode") == "ASCII":
        print('\033[H\033[J', end='', flush=True)
    elif config.get_value("clear_mode") == "command":
        os.system("cls" if os.name == "nt" else "clear")
    elif config.get_value("clear_mode") == "ASCII2":
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


def err(msg) -> None:
    """
    Prints message with err color.

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
