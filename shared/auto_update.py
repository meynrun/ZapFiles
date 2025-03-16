import os

import requests
import tqdm

import sys

from env import VERSION
from shared.localization import lang
from cli import info, err, success


def download_update() -> None:
    """
    Downloads Setup-x64.exe from latest release on GitHub.

    Returns:
        None
    """
    update_setup = requests.get("https://github.com/meynrun/ZapFiles/releases/latest/download/Setup-x64.exe", stream=True)
    total_size = int(update_setup.headers.get("content-length", 0))
    block_size = 1024

    with tqdm.tqdm(total=total_size, unit="B", unit_scale=True, desc="Setup-x64.exe") as pbar:
        with open("Setup-x64.exe", "wb") as f:
            for data in update_setup.iter_content(block_size):
                f.write(data)
                pbar.update(len(data))

    if total_size != 0 and pbar.n != total_size:
        err(lang.get_string("update.error.updateDownloadFailed"))
        os.remove("Setup-x64.exe")
    else:
        success(lang.get_string("update.info.updateDownloaded"))
        os.startfile("Setup-x64.exe")
        sys.exit(0)


def check_for_updates() -> None:
    """
    Checks for updates and calls download_update() if new version is available and user wants to update.

    Returns:
        None
    """
    info(lang.get_string("update.info.checkingForUpdates"))
    try:
        response = requests.get(f"https://api.github.com/repos/meynrun/ZapFiles/releases/latest", timeout=3)

        if response.status_code == 200:
            latest_version = response.json()["tag_name"]

            if latest_version != VERSION:
                info(lang.get_string("update.info.updateAvailable").format(latest_version))
                update = input(lang.get_string("update.info.updateUser")) or "y"
                if update.lower() == "y":
                    info(lang.get_string("update.info.updateDownloading"))
                    download_update()
            else:
                success(lang.get_string("update.info.latestVersion"))
    except requests.exceptions.ConnectTimeout:
        err(lang.get_string("update.error.connectionTimedOut"))
    except requests.exceptions.ConnectionError:
        err(lang.get_string("update.error.connectionError"))
    print("\n")


if __name__ == "__main__":
    check_for_updates()