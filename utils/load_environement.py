import json
from data.var import envFilePath
from utils.json_manager import load_json

def load_enviroment():
    """
    Load the environment file and return the data as a dictionary
    
    Returns:
        dict: The data from the environment file
    """
    return load_json(envFilePath)

def load_enviroment_lang():
    """
    Load the language from the environment file
    
    Returns:
        str: The language from the environment file
    """
    try:
        return json.load(open(envFilePath, "r"))["LANGUAGE"].upper()
    except:
        return "EN"

def load_enviroment_token():
    """
    Load the token from the environment file
    
    Returns:
        str: The token from the environment file
    """
    return json.load(open(envFilePath, "r"))["TOKEN"]