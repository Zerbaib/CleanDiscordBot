from data.var import configFilesFolder
from utils.json_manager import json_save
from utils.logger import *

class Creator():
    def config_folder():
        if not os.path.exists(configFilesFolder):
            printWarn("Code: 404")
            printWarn("No Config Folder found")
            try:
                os.mkdir(configFilesFolder)
                printLog("Config folder created")
            except OSError as e:
                printError("Code: 102")
                printError(f"During creation of {configFilesFolder}")
                printError(e)
                exit(code=102)
            except Exception as e:
                printError("Code: 0")
                printError(f"During creation of {configFilesFolder}")
                printError(e)
                exit(code=0)
    def data_files():
        if dataFileLoad:
            for files in dataFilePath.values():
                if not os.path.exists(files):
                    try:
                        json_save(files, {})
                        printLog(f"{files} was created")
                    except Exception as e:
                        printError("Code: 101")
                        printError(f"During creation of {files}")
                        exit(code=101)
        else:
            printWarn("Code: 301")
            printWarn("The data files creation was desactivate")