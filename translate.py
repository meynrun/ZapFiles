import ctypes
import json
import os
import re
from locale import windows_locale, getlocale

from config_file import config
import cli


def remove_emojis(text: str) -> str:
    """
    Removes emojis from given string.

    Args:
        text (str): Text to remove emojis from.

    Returns:
        str: Text with emojis removed.
    """
    return re.sub(r"[\U0001F000-\U0001FAFF]\s*", "", text)


class Translatable:
    def __init__(self, enable_emojis: bool = True):
        """
        Args:
            enable_emojis (bool, optional): Enables emojis. Defaults to True.
        """
        self.locale = self.get_locale()
        self.enable_emojis = enable_emojis
        self.translated_dict = self._load_translations()

    def get_locale(self) -> str:
        """
        Defines the user language.

        Returns:
            str: The user language code.
        """
        # If self.locale already defined returning it
        if hasattr(self, "locale") and self.locale:
            return self.locale

        if config["language"] == "auto":
            if os.name == "nt":
                windll = ctypes.windll.kernel32
                locale = windows_locale.get(windll.GetUserDefaultUILanguage(), "en_US")
            else:
                locale = getlocale()[0] or "en_US"

            self.locale = "ru" if locale.startswith("ru") else "en"
        else:
            self.locale = config["language"] if config["language"] in ["en", "ru"] else "en"

        return self.locale

    def _load_translations(self) -> dict[str, str]:
        """
        Loads the translation dictionary.

        Returns:
            dict[str, str]: Translation dictionary.
        """
        def load_file(path: str) -> dict[str, str] | None:
            """
            Loads the translation dictionary from a file.

            Args:
                path (str): File path.

            Returns:
                dict[str, str] | None: Translation dictionary or None.
            """
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except FileNotFoundError:
                cli.err(f"❌ Localization file '{path}' not found.")
            except json.decoder.JSONDecodeError:
                cli.err(f"❌ Localization file '{path}' is corrupted.")
            return None  # Returning None if localization file corrupted or doesn't exist

        # Trying to load language json
        translations = load_file(f"lang/{self.locale}.json")

        # If the localization file is corrupted or does not exist, fall back to the English language
        if translations is None and self.locale != "en":
            cli.err("⚠️ Falling back to English.")
            translations = load_file("lang/en.json")

        # If there's not even English, closing app
        if translations is None:
            input("Press Enter to exit...")
            exit(1)

        if not self.enable_emojis:
            translations = {key: remove_emojis(value) for key, value in translations.items()}

        return translations

    def get_string(self, translation_key: str) -> str:
        """
        Retrieves the translated string for a given key.

        Args:
            translation_key (str): The key associated with the desired translation.

        Returns:
            str: The translated string if found, otherwise an error message.
        """

        if translation_key in self.translated_dict:
            return self.translated_dict[translation_key]
        else:
            return f"❌ Translation for '{translation_key}' not found."


lang = Translatable(
    enable_emojis=
        True if config["enable_emojis"]
        else False
)