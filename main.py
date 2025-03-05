import asyncio
import shared

from config_file import config
from auto_update import check_for_updates

from server import server
from client import client

if __name__ == '__main__':
    try:
        shared.clear_console()
        shared.title()
        shared.update()

        if config["check_for_updates"]:
            check_for_updates()
        else:
            pass

        mode = "1" if input(shared.lang["main.choose.mode"]) == "1" else "2"

        shared.clear_console()
        shared.title()

        if mode == "1":
            asyncio.run(server())
        elif mode == "2":
            asyncio.run(client())

        input(shared.lang["main.enterToExit"])

    except KeyboardInterrupt:
        exit()
