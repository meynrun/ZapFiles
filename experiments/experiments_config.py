import json

from shared import error, lang, warn

default_experiments = {
    "file_classification": {
        "name": "File Classification",
        "description": "Classify files based on their file extension.",
        "enabled": False
    },
    "password_protection": {
        "name": "Password Protection (WIP, coming soon)",
        "description": "Protect files on server with a password.",
        "enabled": False
    }
}

def create_default_experiments_configuration_file() -> None:
    """
    Creates a default experiments configuration file.

    Returns:
        None
    """
    with open("experiments.json", "w") as f:
        json.dump(default_experiments, f, indent=4)


def load_experiments_configuration_file() -> dict:
    """
    Loads experiments configuration file.

    Returns:
        Dict: experiments configuration file
    """
    try:
        with open("experiments.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        warn(lang["experiments.warn.experimentsConfigNotFound"])
        try:
            create_default_experiments_configuration_file()
        except Exception as e:
            error(lang["universal.error.generic"].format(str(e)))
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
