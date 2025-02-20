import asyncio
import shared

from experiments import experiments_config
from auto_update import check_for_updates

from server import server
from client import client

if __name__ == '__main__':
    try:
        shared.title()
        shared.update()

        if "config_file" in experiments_config.enabled_experiments:
            from experiments import config_file
            if config_file.config["check_for_updates"]:
                check_for_updates()
            else:
                pass
        else:
            check_for_updates()

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
