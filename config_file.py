import json

default_config = {
    "check_for_updates": True,
    "language": "auto",
    "enable_emojis": True
}


def save_config(config_to_load: dict) -> None:
    """
    Saves config file.

    Args:
        config_to_load (dict): config
    """
    with open("config.json", "w") as f:
        json.dump(config_to_load, f, indent=4)


def check_for_errors(lang_dict: dict[str]) -> None:
    """
    Checks for errors in config file.

    Returns:
        None
    """
    for key in default_config.keys():
        if key not in lang_dict.keys():
            lang_dict[key] = default_config[key]


def load_config() -> dict:
    """
    Loads config file.

    Returns:
        Dict: config
    """
    try:
        with open("config.json", "r") as f:
            lang_dict = json.load(f)
            check_for_errors(lang_dict)
            return lang_dict
    except FileNotFoundError:
        save_config(default_config)
        return default_config
    except json.JSONDecodeError:
        save_config(default_config)
        return default_config
    except Exception as e:
        raise e


config = load_config()
