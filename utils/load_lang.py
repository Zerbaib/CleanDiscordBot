import json

from utils.load_environement import load_enviroment_lang


def load_language_file(file_name):
    """
    Load a language file.

    Args:
        file_name (str): The name of the language file to load.

    Returns:
        dict: The loaded language data.
    """
    try:
        return json.load(open(f"lang/{load_enviroment_lang()}/{file_name}.json", "r", encoding="utf-8"))
    except Exception as e:
        print(f"An error occurred while loading the {file_name} language file")
        print(e)
        return {}


main_lang = load_language_file("main")
casino_lang = load_language_file("casino")
economy_lang = load_language_file("economy")
games_lang = load_language_file("games")
info_lang = load_language_file("info")
mods_lang = load_language_file("mods")
other_lang = load_language_file("other")
owner_lang = load_language_file("owner")
rank_lang = load_language_file("rank")
welcome_lang = load_language_file("welcome")
giveaway_lang = load_language_file("giveaway")