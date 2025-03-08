from base_configuration import BaseConfig

DEFAULT_CONFIG = {
    "check_for_updates": True,
    "language": "auto",
    "enable_emojis": True,
    "clear_mode": "ASCII"
}


class Configuration(BaseConfig):
    def __init__(self, config_path: str):
        super().__init__(config_path, DEFAULT_CONFIG)


config = Configuration("config/config.json")