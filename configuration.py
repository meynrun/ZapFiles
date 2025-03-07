import json
from typing import Any

DEFAULT_CONFIG = {
    "check_for_updates": True,
    "language": "auto",
    "enable_emojis": True,
    "clear_mode": "ASCII"
}


def fix_possible_errors(config_dict: dict[str, str]) -> dict[str, str]:
    """
    Checks for errors in config file.

    Args:
        config_dict (dict[str, str]): Configuration dictionary.

    Returns:
        None
    """
    for key in DEFAULT_CONFIG.keys():
        if key not in config_dict.keys():
            config_dict[key] = DEFAULT_CONFIG[key]

    return config_dict


class Config:
    def __init__(self):
        self.config_file = "config.json"
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """
        Loads config file.

        Returns:
            Dict: config
        """
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config_dict = json.load(f)
                return fix_possible_errors(config_dict)
        except FileNotFoundError:
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        except json.JSONDecodeError:
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        except Exception as e:
            raise e

    def get_value(self, key: str) -> Any:
        """
        Retrieves a value from the configuration dictionary.

        Args:
            key (str): The key associated with the desired value.

        Returns:
            Any: The value stored in the configuration.

        Raises:
            KeyError: If the specified key is not found in the configuration.
        """
        if key not in self.config.keys():
            raise KeyError
        return self.config[key]


def save_config(config_to_load: dict) -> None:
    """
    Saves config file.

    Args:
        config_to_load (dict): config
    """
    with open("config.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(config_to_load, indent=4, ensure_ascii=False))


config = Config()
