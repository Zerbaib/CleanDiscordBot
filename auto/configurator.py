from data.code import Code
from data.var import *
from utils.json_manager import json_save
from utils.logger import *



class Configurator():
    def env_file(self, lang):
        if os.path.exists(envFilePath):
            return
        token = input(lang.get("QUESTION_BOT_TOKEN"))
        while True:
            try:
                lang_choice = input(lang.get("QUESTION_LANGUAGE")).upper()
                if lang_choice in langPossible:
                    lang_choice = lang_choice.upper()
                    break
            except (EOFError, KeyboardInterrupt):
                printError(lang.get("ERROR_EOF_ERROR"))

        with open(envFilePath, 'w'):
            envData = {
                "LANGUAGE": lang_choice,
                "TOKEN": token
            }
            json_save(envFilePath, envData)