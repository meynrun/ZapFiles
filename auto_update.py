import os

import requests
import tqdm

from env import VERSION
from shared import lang

def download_update():
    update_setup = requests.get("https://github.com/meynrun/ZapFiles/releases/latest/download/Setup-x64.exe", stream=True)
    total_size = int(update_setup.headers.get("content-length", 0))
    block_size = 1024

    with tqdm.tqdm(total=total_size, unit="B", unit_scale=True, desc="Setup-x64.exe") as pbar:
        with open("Setup-x64.exe", "wb") as f:
            for data in update_setup.iter_content(block_size):
                f.write(data)
                pbar.update(len(data))

    if total_size != 0 and pbar.n != total_size:
        print(lang["main.info.updateDownloadFailed"])
        os.remove("Setup-x64.exe")
    else:
        print(lang["main.info.updateDownloaded"])
        os.startfile("Setup-x64.exe")
        exit(0)


def check_for_updates():
    response = requests.get(f"https://api.github.com/repos/meynrun/ZapFiles/releases/latest")

    if response.status_code == 200:
        latest_version = response.json()["tag_name"]
        if latest_version != VERSION:
            print(lang["main.info.updateAvailable"].format(latest_version))
            update = input(lang["main.info.updateUser"]) or "y"
            if update.lower() == "y":
                print(lang["main.info.updateDownloading"])
                download_update()


if __name__ == "__main__":
    check_for_updates()