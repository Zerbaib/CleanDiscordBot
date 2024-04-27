from json import dump, load

def load_json(file_path):
    try:
        return load(open(file_path, 'r'))
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except Exception as e:
        print(f"An error occurred while loading the file {file_path}: {e}")
        return {}

def save_json(file_path, data):
    try:
        dump(data, open(file_path, 'w'), indent=4)
    except Exception as e:
        print(f"An error occurred while saving the file {file_path}: {e}")
        return
