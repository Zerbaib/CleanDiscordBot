from data.code import Code
from data.var import *
from utils.json_manager import json_save
from utils.logger import *



class Creator():
    def config_folder():
        if os.path.exists(configFilesFolder):
            return
        printWarn("Code: 404")
        printWarn("No Config Folder found")
        try:
            os.mkdir(configFilesFolder)
            printLog("Config folder created")
        except OSError as e:
            printError("Code: 102")
            printError(f"During creation of {configFilesFolder}")
            printError(e)
            exit(code=Code.FAILED_TO_CREATE_FOLDER)
        except Exception as e:
            printError("Code: 0")
            printError(f"During creation of {configFilesFolder}")
            printError(e)
            exit(code=Code.DEFAULT_ERROR)
    def data_files():
        if dataFileLoad:
            for files in dataFilePath.values():
                if not os.path.exists(files):
                    printWarn("Code: 404")
                    printWarn(f"No {files} was found")
                    try:
                        json_save(files, {})
                        printLog(f"{files} was created")
                    except Exception as e:
                        printError("Code: 101")
                        printError(f"During creation of {files}")
                        printError(e)
                        exit(code=Code.FAILED_TO_CREATE_FILE)
        else:
            printWarn("Code: 301")
            printWarn("The data files creation was desactivate")
    def badword_file():
        if os.path.exists(badWordFilePath):
            return
        printWarn("Code: 404")
        printWarn(f"No {badWordFilePath} was found")
        try:
            badword_data = {
                "bad_words": [
                    "badword1",
                    "badword2",
                    "badword3"
                ]
            }
            json_save(badWordFilePath, badword_data)
            printLog(f"{badWordFilePath} was created")
        except Exception as e:
            printError("Code: 101")
            printError(f"During creation of {badWordFilePath}")
            printError(e)
            exit(code=Code.FAILED_TO_CREATE_FILE)