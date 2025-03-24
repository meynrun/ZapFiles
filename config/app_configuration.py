import os.path

from config.base_configuration import BaseConfig
from env import ROOT_DIR

from getpass import getuser


DEFAULT_CONFIG = {
    "check_for_updates": True,
    "language": "auto",
    "enable_emojis": True,
    "clear_mode": "ASCII",
    "downloads_path": f"C:/Users/{getuser()}/Downloads/ZapFiles Downloads/"
}


class Configuration(BaseConfig):
    def __init__(self, config_path: str):
        super().__init__(config_path, DEFAULT_CONFIG)
        self._check_downloads_path()

    def _check_downloads_path(self):
        if not os.path.isdir(self.get_value("downloads_path")) or not os.path.exists(self.get_value("downloads_path")):
            print("Config path does not exist or is not a directory, using default path")
            self.config["downloads_path"] = self.default_config["downloads_path"]


config = Configuration(os.path.join(ROOT_DIR, "config", "config.json"))