from modules.var import files
from utils.json_manager import json_load


def load_enviroment():
    """
    Load the environment file and return the data as a dictionary

    Returns:
        dict: The data from the environment file
    """
    return json_load(files.env)

def load_enviroment_lang():
    """
    Load the language from the environment file

    Returns:
        str: The language from the environment file
    """
    try:
        return json_load(files.env)["LANGUAGE"].upper()
    except Exception:
        return "EN"

def load_enviroment_token():
    """
    Load the token from the environment file

    Returns:
        str: The token from the environment file
    """
    return json_load(files.env)["TOKEN"]