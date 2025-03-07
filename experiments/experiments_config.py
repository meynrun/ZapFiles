import json
import os

from cli import err
from translate import lang

DEFAULT_EXPERIMENTS = {
    "file_classification": {
        "name": lang.get_string("experiments.file_classification.name"),
        "description": lang.get_string("experiments.file_classification.description"),
        "enabled": False
    }
}

class ExperimentsConfig:
    def __init__(self):
        self.experiments_file = "./config/experiments.json"
        os.makedirs(os.path.dirname(self.experiments_file), exist_ok=True)
        self.experiments = self.load_experiments_configuration_file()
        self.enabled_experiments = self.get_enabled_experiments()

    def load_experiments_configuration_file(self) -> dict:
        """
        Loads experiments configuration file.

        Returns:
            Dict: experiments configuration file
        """
        try:
            with open(self.experiments_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            try:
                self.create_default_experiments_configuration_file()
            except Exception as e:
                err(lang.get_string("universal.err.generic").format(str(e)))
            return DEFAULT_EXPERIMENTS

    def get_enabled_experiments(self) -> dict:
        """
        Gets enabled experiments from experiments configuration file.

        Returns:
            Dict: enabled experiments
        """
        if hasattr(self, "enabled_experiments") and self.enabled_experiments:
            return self.enabled_experiments
        else:
            return {key: value for key, value in self.experiments.items() if value["enabled"]}

    def create_default_experiments_configuration_file(self) -> None:
        """
        Creates a default experiments configuration file.

        Returns:
            None
        """
        with open(self.experiments_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(DEFAULT_EXPERIMENTS, indent=4, ensure_ascii=False))


experiments_config = ExperimentsConfig()