import os
import platform
from datetime import datetime, timezone

import aiohttp
import disnake
from auto.configurator import Configurator
from auto.creator import Creator
from data.code import Code
from data.var import *
from disnake.ext import commands
from utils.json_manager import json_load, json_save
from utils.load_environement import load_enviroment_lang, load_enviroment_token
from utils.load_lang import main_lang
from utils.logger import *
from utils.sql_manager import *



get_next_log_file()
initDB()
lang = main_lang
self = None

printInfo("Starting ...")

Creator.config_folder()
Creator.data_files()
Creator.badword_file()

printInfo("Files creation done")

Configurator.env_file(self, lang)

printLog("Reload lang ...")
lang = main_lang
printLog("lang Reloaded")

printInfo("Files configuration done")

if not os.path.exists(configFilePath):
    with open(configFilePath, 'w'):
        prefix = input(lang.get("QUESTION_PREFIX"))
        logID = int(input(lang.get("QUESTION_LOG_CHANNEL_ID")))
        pollID = int(input(lang.get("QUESTION_POLL_CHANNEL_ID")))
        joinID = int(input(lang.get("QUESTION_WELCOME_CHANNEL_ID")))
        leaveID = int(input(lang.get("QUESTION_LEAVE_CHANNEL_ID")))
        voiceID = int(input(lang.get("QUESTION_VOICE_CHANNEL_ID")))
        ownerID = int(input(lang.get("QUESTION_OWNER_ID")))
        muteID = int(input(lang.get("QUESTION_MUTE_ROLE_ID")))
        rank1 = int(input(lang.get("QUESTION_XP_ROLE_10_ID")))
        rank2 = int(input(lang.get("QUESTION_XP_ROLE_25_ID")))
        rank3 = int(input(lang.get("QUESTION_XP_ROLE_50_ID")))
        config_data = {
            "PREFIX": prefix,
            "LOG_ID": logID,
            "POLL_ID": pollID,
            "JOIN_ID": joinID,
            "LEAVE_ID": leaveID,
            "AUTO_VOICE_ID": voiceID,
            "YOUR_ID": ownerID,
            "MUTE_ROLE_ID": muteID,
            "del_time": 3,
            "level_roles": {
                "10": rank1,
                "25": rank2,
                "50": rank3
            }
        }
        json_save(configFilePath, config_data)

try:
    config = json_load(configFilePath)
except Exception as e:
    print(lang.get("ERROR_CONFIG_LOAD").format(e))
    exit(1)

prefix = config["PREFIX"]
botLang = load_enviroment_lang()

bot = commands.Bot(
    command_prefix=prefix,
    intents=disnake.Intents.all(),
    case_insensitive=True
)
bot.remove_command('help')

@bot.event
async def on_ready():
    if bot.user.discriminator == 0:
        botName = bot.user.name
    else:
        botName = f"{bot.user.name}#{bot.user.discriminator}"

    async with aiohttp.ClientSession() as session:
        async with session.get(onlineVersion) as response:
            botRepoVersion = await response.text() if response.status == 200 else "Unknown"

    with open(localVersionFilePath, 'r') as version_file:
        botVersion = version_file.read().strip()

    if botVersion != botRepoVersion:
        print('='*multiplicator)
        printWarn(lang.get("HEADER_OUTDATED_LN1"))
        printWarn(lang.get("HEADER_OUTDATED_LN2"))
        printWarn(lang.get("HEADER_OUTDATED_LN3"))
    print('='*multiplicator)
    printInfo(lang.get("HEADER_LN1").format(reset=reset))
    printInfo(lang.get("HEADER_LN2").format(botName=botName, botId=bot.user.id, reset=reset, blue=blue))
    printInfo(lang.get("HEADER_LN3").format(amount=len(bot.guilds), reset=reset, blue=blue))
    printInfo(lang.get("HEADER_LN4").format(language=botLang, reset=reset, blue=blue))
    printInfo(lang.get("HEADER_LN5").format(prefix=prefix, reset=reset, blue=blue))
    printInfo(lang.get("HEADER_LN6").format(owner=bot.get_user(config["YOUR_ID"]), reset=reset, blue=blue))
    printInfo(lang.get("HEADER_LN7").format(gitBranch=gitBranch, reset=reset, blue=blue))
    printInfo(lang.get("HEADER_LN8").format(botVersion=botVersion, reset=reset, blue=blue))
    printInfo(lang.get("HEADER_LN9").format(botRepoVersion=botRepoVersion, reset=reset, blue=blue))
    printInfo(lang.get("HEADER_LN10").format(apiVersion=disnake.__version__, reset=reset, blue=blue))
    printInfo(lang.get("HEADER_LN11").format(platformSystem=platform.system(), platformVersion=platform.release(), osName=os.name, reset=reset, blue=blue))
    printInfo(lang.get("HEADER_LN12").format(pythonVersion=platform.python_version(), reset=reset, blue=blue))
    printInfo(lang.get("HEADER_LN13").format(timeNow=datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M:%S"), reset=reset, blue=blue))
    print('='*multiplicator)
    return

for element in os.listdir(cogsFolder):
    try:
        element_dir = f"{cogsFolder}{element}"
        if os.path.isdir(element_dir):
            for filename in os.listdir(element_dir):
                if filename.endswith('.py'):
                    cog_name = filename[:-3]
                    try:
                        bot.load_extension(f'cogs.{element}.{cog_name}')
                    except Exception as e:
                        printError(lang.get("ERROR_COG_LOADING").format(cogName=cog_name, e=e))
    except Exception as e:
        printError(lang.get("ERROR_ELEMENTS_LOADING").format(element, e))
        exit(code=1)



try:
    bot.run(load_enviroment_token())
except Exception as e:
    printError("Code: 301")
    printError("Error during the token loading")
    printError("Change the token")
    exit(code=Code.SETTINGS_WARNING)
