import os.path

from config.base_configuration import BaseConfig
from env import ROOT_DIR
from shared.localization import lang

DEFAULT_EXPERIMENTS = {
    "file_classification": {
        "name": lang.get_string("experiments.file_classification.name"),
        "description": lang.get_string("experiments.file_classification.description"),
        "enabled": False
    }
}


class ExperimentsConfig(BaseConfig):
    def __init__(self, config_path: str):
        super().__init__(config_path, DEFAULT_EXPERIMENTS)
        self.enabled_experiments = self.get_enabled_experiments()

    def get_enabled_experiments(self) -> dict[str, dict[str, bool]]:
        """
        Gets enabled experiments from experiments configuration file.

        Returns:
            Dict: enabled experiments
        """
        if hasattr(self, "enabled_experiments") and self.enabled_experiments:
            return self.enabled_experiments
        else:
            return {key: value for key, value in self.config.items() if value["enabled"]}


experiments_config = ExperimentsConfig(os.path.join(ROOT_DIR, "config", "experiments.json"))