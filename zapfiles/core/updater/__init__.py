import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import Any

import questionary
import requests
import tqdm

from zapfiles.cli import info, err, success
from zapfiles.constants import VERSION
from zapfiles.core.hash import get_file_hash
from zapfiles.core.localization import lang


def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)  # type: ignore[attr-defined] # because pylance fails on os != windows
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", path])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", path])
    else:
        print("Unsupported platform")


def download_update(assets: list[dict[str, Any]]) -> None:
    """
    Downloads Setup-x64.exe from latest release on GitHub.

    Returns:
        None
    """
    if os.name != "nt":
        err(lang.get_string("update.error.platformNotSupported"))
        return

    for asset in assets:
        if asset.get("name") == "Setup-x64.exe":
            update_setup = requests.get(
                asset.get("browser_download_url"), stream=True, verify=True
            )

            total_size = int(update_setup.headers.get("content-length", 0))
            block_size = 1024

            with tqdm.tqdm(
                total=total_size, unit="B", unit_scale=True, desc="Setup-x64.exe"
            ) as pbar:
                with open("Setup-x64.exe", "wb") as f:
                    for data in update_setup.iter_content(block_size):
                        f.write(data)
                        pbar.update(len(data))

            if total_size != 0 and pbar.n != total_size:
                err(lang.get_string("update.error.updateDownloadFailed"))
                os.remove("Setup-x64.exe")
                return
            else:
                success(lang.get_string("update.info.updateDownloaded"))

                info(lang.get_string("client.hash.checking"))
                downloaded_file_hash = get_file_hash(Path("Setup-x64.exe"))
                valid_hash = asset.get("digest")[7:]

                if downloaded_file_hash != valid_hash:
                    err(lang.get_string("client.hash.incorrect"))
                    err(lang.get_string("update.error.updateDownloadFailed"))
                    os.remove("Setup-x64.exe")
                    return

                open_file("Setup-x64.exe")
                sys.exit(0)


def check_for_updates() -> None:
    """
    Checks for updates and calls download_update() if new version is available and user wants to update.

    Returns:
        None
    """
    info(lang.get_string("update.info.checkingForUpdates"))
    try:
        response = requests.get(
            "https://api.github.com/repos/meynrun/ZapFiles/releases/latest",
            timeout=3,
            verify=True,
        )

        if response.status_code == 200:
            response_json = response.json()
            latest_version = response_json.get(
                "tag_name", f"v{VERSION}"
            )  # if, for some reason, there is no tag_name, fall back to the currently installed version

            if latest_version != f"v{VERSION}":
                info(
                    lang.get_string("update.info.updateAvailable").format(
                        latest_version
                    )
                )
                update = questionary.confirm(
                    lang.get_string("update.info.confirmUpdate")
                ).ask()
                if update:
                    info(lang.get_string("update.info.updateDownloading"))
                    download_update(response_json.get("assets", []))
            else:
                success(lang.get_string("update.info.latestVersion"))
    except requests.exceptions.ConnectTimeout:
        err(lang.get_string("update.error.connectionTimedOut"))
    except requests.exceptions.ConnectionError:
        err(lang.get_string("update.error.connectionError"))
    print("\n")


if __name__ == "__main__":
    check_for_updates()
