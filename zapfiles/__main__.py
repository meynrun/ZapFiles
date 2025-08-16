import asyncio
import ctypes
import json
import os
import sys
from pathlib import Path
import questionary

from zapfiles.cli import clear_console, title
from zapfiles.client import client, connect
from zapfiles.core.config.app_configuration import config
from zapfiles.core.localization import lang
from zapfiles.core.updater import check_for_updates
from zapfiles.server import server


async def handle_zapfile() -> int:
    if len(sys.argv) > 1:
        try:
            file_path = Path(sys.argv[1])
            if file_path.is_file():
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    host = data.get("host", "localhost")
                    port = data.get("port", 8888)
                    filename = data.get("filename", "filename")
                    file_hash = data.get("hash", "hash")
                    await connect(host, port, filename, file_hash)
                    return 1
        except Exception as e:
            print(e)
    return 0


def main() -> None:
    if os.name == "nt":
        windll = ctypes.windll.kernel32
        windll.SetConsoleTitleW(
            "⚡ZapFiles" if config.get_value("enable_emojis") else "ZapFiles"
        )

    try:
        clear_console()
        title()

        if (
            asyncio.run(handle_zapfile()) == 1
        ):  # if argv[1] was a valid zapfile then return
            return

        if config.get_value("check_for_updates"):
            check_for_updates()

        choices = [
            {"name": lang.get_string("main.mode.host"), "value": "host"},
            {"name": lang.get_string("main.mode.get"), "value": "get"},
        ]

        mode = questionary.select(
            message=lang.get_string("main.mode.select"), choices=choices
        ).ask()

        clear_console()
        title()

        if mode == "host":
            asyncio.run(server())
        elif mode == "get":
            asyncio.run(client())
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
    try:
        input(lang.get_string("main.enterToExit"))
    except KeyboardInterrupt:
        pass
