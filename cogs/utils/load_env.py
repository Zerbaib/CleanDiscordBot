import json

def load_enviroment():
    with open(".env", "r") as file:
        return json.load(file)

def load_enviroment_lang():
    with open(".env", "r") as file:
        return json.load(file)["LANGUAGE"]

def load_enviroment_token():
    with open(".env", "r") as file:
        return json.load(file)["TOKEN"]