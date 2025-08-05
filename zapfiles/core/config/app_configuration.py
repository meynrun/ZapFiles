import os
from getpass import getuser
from os import PathLike
from pathlib import Path

from zapfiles.constants import ROOT_DIR
from zapfiles.core.config.base_configuration import BaseConfig


def get_default_download_directory():
    if os.name == "nt":
        return f"C:\\Users\\{getuser()}\\Downloads\\ZapFiles Downloads\\"
    else:
        return Path(ROOT_DIR) / "ZapFiles Downloads"


DEFAULT_CONFIG = {
    "check_for_updates": True,
    "language": "auto",
    "enable_emojis": True,
    "clear_mode": "ASCII",
    "downloads_path": str(get_default_download_directory()),
    "enable_tips": True,
}


class Configuration(BaseConfig):
    def __init__(self, config_path: PathLike[str]):
        super().__init__(config_path, DEFAULT_CONFIG)
        self._check_downloads_path()

    def _check_downloads_path(self):
        downloads_path = Path(self.get_value("downloads_path"))
        if not downloads_path.exists() or not downloads_path.is_dir():
            print(
                "Config path does not exist or is not a directory, using default path"
            )
            self.config["downloads_path"] = self.default_config["downloads_path"]


config = Configuration(Path(ROOT_DIR) / "config" / "config.json")
