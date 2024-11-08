import asyncio
import shared as shared

from server import server
from client import client

from shared import lang
from auto_update import check_for_updates

if __name__ == '__main__':
    shared.title()
    check_for_updates()

    shared.clear_console()

    mode = "1"\
        if input(lang["main.choose.mode"]) == "1"\
        else "2"

    shared.clear_console()

    if mode == "1":
        asyncio.run(server())
    elif mode == "2":
        asyncio.run(client())

    input(lang["main.enterToExit"])
