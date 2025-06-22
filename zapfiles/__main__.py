import asyncio
import ctypes
import json
import os
import sys
from pathlib import Path

from zapfiles.cli import clear_console, title, color, ColorEnum
from zapfiles.client import client, connect
from zapfiles.core.config.app_configuration import config
from zapfiles.core.config.experiments_configuration import experiments_config
from zapfiles.core.localization import lang
from zapfiles.core.updater import check_for_updates
from zapfiles.server import server


def get_modes() -> str:
    if "lan_broadcast" in experiments_config.get_enabled_experiments():
        return (
            lang.get_string("main.choose.mode") +
            lang.get_string("experiments.lan_broadcast.mode") +
            lang.get_string("main.input")
            )
    return (
            lang.get_string("main.choose.mode") +
            lang.get_string("main.input")
    )


async def handle_zapfile() -> int:
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        if file_path.is_file():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                host = data.get("host", "localhost")
                port = data.get("port", 8888)
                filename = data.get("filename", "filename")
                file_hash = data.get("hash", "hash")
                await connect(host, port, filename, file_hash)
                return 1
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

        if asyncio.run(handle_zapfile()) == 1:
            return

        if config.get_value("check_for_updates"):
            check_for_updates()

        mode = (
            input(
                color(
                    get_modes(),
                    ColorEnum.WARN,
                    ColorEnum.SUCCESS,
                ) or "2"
            )
        )

        clear_console()
        title()

        if mode == "1":
            asyncio.run(server())
        elif mode == "2":
            asyncio.run(client())

        if "lan_broadcast" in experiments_config.get_enabled_experiments() and mode == "3":
            # TODO: lan broadcast
            pass

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
    input(lang.get_string("main.enterToExit"))
