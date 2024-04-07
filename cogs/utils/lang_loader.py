import json
from cogs.utils.load_env import load_enviroment_lang

lang = load_enviroment_lang()

def load_casino_lang():
    with open(f"lang/{lang}/casino.json", "r") as file:
        return json.load(file)

def load_economy_lang():
    with open(f"lang/{lang}/economy.json", "r") as file:
        return json.load(file)