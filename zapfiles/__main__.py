import asyncio
import ctypes
import os
import sys

from zapfiles.cli import clear_console, title, color, ColorEnum
from zapfiles.client import client
from zapfiles.core.config.app_configuration import config
from zapfiles.core.localization import lang
from zapfiles.core.updater import check_for_updates
from zapfiles.server import server

if __name__ == "__main__":
    if os.name == "nt":
        windll = ctypes.windll.kernel32
        windll.SetConsoleTitleW(
            "⚡ZapFiles" if config.get_value("enable_emojis") else "ZapFiles"
        )

    try:
        clear_console()
        title()

        if config.get_value("check_for_updates"):
            check_for_updates()
        else:
            pass

        mode = (
            "1"
            if input(
                color(
                    lang.get_string("main.choose.mode"),
                    ColorEnum.WARN,
                    ColorEnum.SUCCESS,
                )
            )
            == "1"
            else "2"
        )

        clear_console()
        title()

        if mode == "1":
            asyncio.run(server())
        elif mode == "2":
            asyncio.run(client())

        input(lang.get_string("main.enterToExit"))

    except KeyboardInterrupt:
        sys.exit(0)
