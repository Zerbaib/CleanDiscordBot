import json
import os

lang = os.environ["LANGUAGE"]

def load_casino_lang():
    with open(f"lang/{lang}/casino.json", "r") as file:
        return json.load(file)
