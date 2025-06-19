import os
from enum import Enum

import colorama as clr
from colorama import Fore

from zapfiles.constants import VERSION
from zapfiles.core.config.app_configuration import config

clr.init()


class ColorEnum(str, Enum):
    INFO = clr.Fore.LIGHTBLUE_EX
    WARN = clr.Fore.LIGHTYELLOW_EX
    ERROR = clr.Fore.LIGHTRED_EX
    SUCCESS = clr.Fore.LIGHTGREEN_EX
    RESET = clr.Style.RESET_ALL

    def __str__(self):
        return self.value


def title() -> None:
    """
    Prints title.

    Returns:
        None
    """
    if config.get_value("enable_emojis"):
        title_text = f"""{Fore.LIGHTYELLOW_EX}ZapFiles {Fore.LIGHTWHITE_EX}v{VERSION}
{Fore.LIGHTYELLOW_EX}Made with 💖 by {Fore.LIGHTBLUE_EX}Meynrun
    """
    else:
        title_text = f"""{Fore.LIGHTYELLOW_EX}ZapFiles {Fore.LIGHTWHITE_EX}v{VERSION}
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
        print("\033[H\033[J", end="", flush=True)
    elif config.get_value("clear_mode") == "command":
        os.system("cls" if os.name == "nt" else "clear")
    elif config.get_value("clear_mode") == "ASCII2":
        print("\x1b[2J\x1b[0;0H", end="", flush=True)


def info(msg: str) -> None:
    """
    Prints message with info color.

    Args:
        msg (str): message to print

    Returns:
        None
    """
    print(color(msg, ColorEnum.INFO))


def warn(msg: str) -> None:
    """
    Prints message with warn color.

    Args:
        msg (str): message to print

    Returns:
        None
    """
    print(color(msg, ColorEnum.WARN))


def err(msg: str) -> None:
    """
    Prints message with err color.

    Args:
        msg (str): message to print

    Returns:
        None
    """
    print(color(msg, ColorEnum.ERROR))


def success(msg: str) -> None:
    """
    Prints message with success color.

    Args:
        msg (str): message to print

    Returns:
        None
    """
    print(color(msg, ColorEnum.SUCCESS))


def color(
    msg: str, color_start: ColorEnum, color_end: ColorEnum = ColorEnum.RESET
) -> str:
    """
    Args:
        msg (str): message
        color_start (ColorEnum): color at the start
        color_end (ColorEnum): color at the end

    Returns:
        str: colorized message string
    """
    return color_start + msg + color_end
