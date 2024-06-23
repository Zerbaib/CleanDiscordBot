from data.var import envFilePath
from utils.json_manager import json_load

def load_enviroment():
    """
    Load the environment file and return the data as a dictionary
    
    Returns:
        dict: The data from the environment file
    """
    with open(envFilePath.name, "r", encoding="utf-8") as file:
        return json_load(file)

def load_enviroment_lang():
    """
    Load the language from the environment file
    
    Returns:
        str: The language from the environment file
    """
    try:
        with open(envFilePath.name, "r", encoding="utf-8") as file:
            return json_load(file)["LANGUAGE"].upper()
    except:
        return "EN"

def load_enviroment_token():
    """
    Load the token from the environment file
    
    Returns:
        str: The token from the environment file
    """
    with open(envFilePath.name, "r", encoding="utf-8") as file:
        return json_load(file)["TOKEN"]