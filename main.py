import asyncio
import shared_functions

from server import server
from client import client

if __name__ == '__main__':
    mode = "1"\
        if input("🚀 Enter mode\n\n 1. Host files\n 2. Get files\n\n>> ") == "1"\
        else "2"

    shared_functions.clear_console()

    if mode == "1":
        asyncio.run(server())
    elif mode == "2":
        asyncio.run(client())

    input()
