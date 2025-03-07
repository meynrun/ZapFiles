import json

from cli import err, warn
from translate import lang

default_experiments = {
    "file_classification": {
        "name": lang.get_string("experiments.file_classification.name"),
        "description": lang.get_string("experiments.file_classification.description"),
        "enabled": False
    }
}

def create_default_experiments_configuration_file() -> None:
    """
    Creates a default experiments configuration file.

    Returns:
        None
    """
    with open("experiments.json", "w", encoding="utf-8") as f:
        json.dump(default_experiments, f, indent=4, ensure_ascii=False)


def load_experiments_configuration_file() -> dict:
    """
    Loads experiments configuration file.

    Returns:
        Dict: experiments configuration file
    """
    try:
        with open("experiments.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        warn(lang.get_string("experiments.warn.experimentsConfigNotFound"))
        try:
            create_default_experiments_configuration_file()
        except Exception as e:
            err(lang.get_string("universal.err.generic").format(str(e)))
        return default_experiments


def load_enabled_experiments() -> dict:
    """
    Loads enabled experiments from experiments configuration file.

    Returns:
        Dict: enabled experiments
    """
    experiments = load_experiments_configuration_file()
    return {key: value for key, value in experiments.items() if value["enabled"]}


enabled_experiments = load_enabled_experiments()
