import json

def load_enviroment():
    with open(".env", "r") as file:
        return json.load(file)

def load_enviroment_lang():
    return json.load(open(".env", "r"))["LANGUAGE"].upper()

def load_enviroment_token():
    return json.load(open(".env", "r"))["TOKEN"]