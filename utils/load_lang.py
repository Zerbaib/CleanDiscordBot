import json
from utils.load_environement import load_enviroment_lang

def load_main_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/main.json", "r"))

def load_casino_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/casino.json", "r"))

def load_economy_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/economy.json", "r"))

def load_games_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/games.json", "r"))

def load_info_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/info.json", "r"))

def load_mods_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/mods.json", "r"))

def load_other_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/other.json", "r"))

def load_owner_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/owner.json", "r"))

def load_rank_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/rank.json", "r"))

def load_welcome_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/welcome.json", "r"))

def load_giveaway_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/giveaway.json", "r"))