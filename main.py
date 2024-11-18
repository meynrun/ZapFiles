import asyncio
import shared
import sys

from server import server
from client import client

from shared import lang
from auto_update import check_for_updates
from gui import gui

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) > 0:
        if args[0] == "--gui":
            gui()

        else:
            shared.error(lang["main.error.unknownArgument"].format(args[0]))
            sys.exit(1)

    else:
        shared.title()
        check_for_updates()

        mode = "1" \
            if input(lang["main.choose.mode"]) == "1" \
            else "2"

        shared.clear_console()
        shared.title()

        if mode == "1":
            asyncio.run(server())
        elif mode == "2":
            asyncio.run(client())

        input(lang["main.enterToExit"])
