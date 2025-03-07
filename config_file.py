import json

default_config = {
    "check_for_updates": True,
    "language": "auto",
    "enable_emojis": True,
    "clear_mode": "ASCII"
}


def save_config(config_to_load: dict) -> None:
    """
    Saves config file.

    Args:
        config_to_load (dict): config
    """
    with open("config.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(config_to_load, indent=4, ensure_ascii=False))


def check_for_errors(config_dict: dict[str]) -> None:
    """
    Checks for errors in config file.

    Args:
        config_dict (dict): config

    Returns:
        None
    """
    for key in default_config.keys():
        if key not in config_dict.keys():
            config_dict[key] = default_config[key]


def load_config() -> dict:
    """
    Loads config file.

    Returns:
        Dict: config
    """
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config_dict = json.load(f)
            check_for_errors(config_dict)
            return config_dict
    except FileNotFoundError:
        save_config(default_config)
        return default_config
    except json.JSONDecodeError:
        save_config(default_config)
        return default_config
    except Exception as e:
        raise e


config = load_config()
