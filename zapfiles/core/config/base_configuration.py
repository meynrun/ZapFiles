import json
import os
from typing import Any


class BaseConfig:
    def __init__(self, config_path: str, default_config: dict[str, Any]):
        self.config_path = config_path
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        self.default_config = default_config
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """
        Loads config file.

        Returns:
            Dict: config
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
                return self._fix_missing_keys()
        except FileNotFoundError:
            self._save_config(self.default_config)
            return self.default_config
        except json.JSONDecodeError:
            self._save_config(self.default_config)
            return self.default_config
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

    def _save_config(self, config_to_save: dict) -> None:
        """
        Saves config file.

        Args:
            config_to_save (dict): config

        Returns:
            None
        """
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(config_to_save, indent=4, ensure_ascii=False))

    def _fix_missing_keys(self) -> dict[str, str]:
        """
        Validates and fixes missing keys in the configuration.

        This method checks if all required keys from the default configuration
        exist in the current configuration. If any key is missing, it is added
        with its default value.

        Returns:
            dict[str, str]: The updated configuration with missing keys fixed.
        """
        for key in self.default_config.keys():
            if key not in self.config:
                self.config[key] = self.default_config[key]

        return self.config
