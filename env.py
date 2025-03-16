from colorama import Fore
from config.app_configuration import config

VERSION = "v1.9.0"

if config.get_value("enable_emojis"):
    TITLE = f"""{Fore.LIGHTYELLOW_EX}ZapFiles {Fore.LIGHTWHITE_EX}{VERSION}
{Fore.LIGHTYELLOW_EX}Made with 💖 by {Fore.LIGHTBLUE_EX}Meynrun
"""
else:
    TITLE = f"""{Fore.LIGHTYELLOW_EX}ZapFiles {Fore.LIGHTWHITE_EX}{VERSION}
{Fore.LIGHTYELLOW_EX}Made with love by {Fore.LIGHTBLUE_EX}Meynrun
"""
