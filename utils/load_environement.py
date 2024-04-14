import json
from data.var import envFilePath

def load_enviroment():
    with open(envFilePath, "r") as file:
        return json.load(file)

def load_enviroment_lang():
    return json.load(open(envFilePath, "r"))["LANGUAGE"].upper()

def load_enviroment_token():
    return json.load(open(envFilePath, "r"))["TOKEN"]