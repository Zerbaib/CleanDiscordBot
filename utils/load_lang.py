import json
from utils.load_environement import load_enviroment_lang

def load_main_lang():
    try:
        return json.load(open(f"lang/{load_enviroment_lang()}/main.json", "r"))
    except Exception as e:
        print("An error occurred while loading the main language file")
        print(e)
        return {}

def load_casino_lang():
    try:
        return json.load(open(f"lang/{load_enviroment_lang()}/casino.json", "r"))
    except Exception as e:
        print("An error occurred while loading the casino language file")
        print(e)
        return {}

def load_economy_lang():
    try:
        return json.load(open(f"lang/{load_enviroment_lang()}/economy.json", "r"))
    except Exception as e:
        print("An error occurred while loading the economy language file")
        print(e)
        return {}

def load_games_lang():
    try:
        return json.load(open(f"lang/{load_enviroment_lang()}/games.json", "r"))
    except Exception as e:
        print("An error occurred while loading the games language file")
        print(e)
        return {}

def load_info_lang():
    try:
        return json.load(open(f"lang/{load_enviroment_lang()}/info.json", "r"))
    except Exception as e:
        print("An error occurred while loading the info language file")
        print(e)
        return {}

def load_mods_lang():
    try:
        return json.load(open(f"lang/{load_enviroment_lang()}/mods.json", "r"))
    except Exception as e:
        print("An error occurred while loading the mods language file")
        print(e)
        return {}

def load_other_lang():
    try:
        return json.load(open(f"lang/{load_enviroment_lang()}/other.json", "r"))
    except Exception as e:
        print("An error occurred while loading the other language file")
        print(e)
        return {}

def load_owner_lang():
    try:
        return json.load(open(f"lang/{load_enviroment_lang()}/owner.json", "r"))
    except Exception as e:
        print("An error occurred while loading the owner language file")
        print(e)
        return {}

def load_rank_lang():
    try:
        return json.load(open(f"lang/{load_enviroment_lang()}/rank.json", "r"))
    except Exception as e:
        print("An error occurred while loading the rank language file")
        print(e)
        return {}

def load_welcome_lang():
    try:
        return json.load(open(f"lang/{load_enviroment_lang()}/welcome.json", "r"))
    except Exception as e:
        print("An error occurred while loading the welcome language file")
        print(e)
        return {}

def load_giveaway_lang():
    try:
        return json.load(open(f"lang/{load_enviroment_lang()}/giveaway.json", "r"))
    except Exception as e:
        print("An error occurred while loading the giveaway language file")
        print(e)
        return {}