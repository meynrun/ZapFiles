import json

default_config = {
    "check_for_updates": True
}


def save_config(config_to_load: dict) -> None:
    """
    Saves config file.

    Args:
        config_to_load (dict): config
    """
    with open("config.json", "w") as f:
        json.dump(config_to_load, f, indent=4)


def load_config() -> dict:
    """
    Loads config file.

    Returns:
        Dict: config
    """
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        save_config(default_config)
        return default_config
    except json.JSONDecodeError:
        save_config(default_config)
        return default_config
    except Exception as e:
        raise e


config = load_config()
