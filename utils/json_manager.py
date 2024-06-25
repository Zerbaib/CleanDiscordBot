from json import dump, load

def json_load(file_path):
    """
    Load a json file and return the data as a dictionary

    Parameters:
        file_path (str): The path to the json file

    Returns:
        dict: The data from the json file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except Exception as e:
        print(f"An error occurred while loading the file {file_path}: {e}")
        return {}

def json_save(file_path, data, intent=4):
    """
    Save a dictionary to a json file

    Parameters:
        file_path (str): The path to the json file
        data (dict): The data to save

    Returns:
        bool: True if the file was saved successfully, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            dump(data, file, indent=intent)
        file.close()
        return True
    except Exception as e:
        print(f"An error occurred while saving the file {file_path}: {e}")
        return False
