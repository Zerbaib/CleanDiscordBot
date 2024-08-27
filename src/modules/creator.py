from modules.code import Code
from modules.var import *
from utils.json_manager import json_save
from utils.logger import *



class Creator():
    def config_folder():
        if os.path.exists(folders.config):
            return
        printWarn("Code: 404")
        printWarn("No Config Folder found")
        try:
            os.mkdir(folders.config)
            printLog("Config folder created")
        except OSError as e:
            printError("Code: 102")
            printError(f"During creation of {folders.config}")
            printError(e)
            exit(code=Code.FAILED_TO_CREATE_FOLDER)
        except Exception as e:
            printError("Code: 0")
            printError(f"During creation of {folders.config}")
            printError(e)
            exit(code=Code.DEFAULT_ERROR)
    def data_files():
        if parameters.dataFileLoad:
            for fs in files.dataFilePath.values():
                if not os.path.exists(fs):
                    printWarn("Code: 404")
                    printWarn(f"No {fs} was found")
                    try:
                        json_save(fs, {})
                        printLog(f"{fs} was created")
                    except Exception as e:
                        printError("Code: 101")
                        printError(f"During creation of {fs}")
                        printError(e)
                        exit(code=Code.FAILED_TO_CREATE_FILE)
        else:
            printWarn("Code: 301")
            printWarn("The data files creation was desactivate")
    def badword_file():
        if os.path.exists(files.badWord):
            return
        printWarn("Code: 404")
        printWarn(f"No {files.badWord} was found")
        try:
            badword_data = {
                "bad_words": [
                    "badword1",
                    "badword2",
                    "badword3"
                ]
            }
            json_save(files.badWord, badword_data)
            printLog(f"{files.badWord} was created")
        except Exception as e:
            printError("Code: 101")
            printError(f"During creation of {files.badWord}")
            printError(e)
            exit(code=Code.FAILED_TO_CREATE_FILE)