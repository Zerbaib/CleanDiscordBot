import json
import os
import platform
import datetime

import aiohttp
import disnake
from disnake.ext import commands

from utils.load_environement import load_enviroment_lang, load_enviroment_token
from utils.load_lang import main_lang
from data.var import *



lang = main_lang

if not os.path.exists(configFilesFolder):
    os.mkdir(configFilesFolder)

if dataFileLoad:
    for files in dataFilePath.values():
        if not os.path.exists(files):
            with open(files, 'w') as file:
                json.dump({}, file)

if not os.path.exists(envFilePath):
    token = input(lang.get("QUESTION_BOT_TOKEN"))
    while True:
        try:
            lang_choice = input(lang.get("QUESTION_LANGUAGE")).upper()
            if lang_choice in langPossible:
                lang_choice = lang_choice.upper()
                break
        except (EOFError, KeyboardInterrupt):
            print(lang.get("ERROR_EOF_ERROR"))
            print(lang.get("ERROR_EOF_ERROR"))
            
    with open(envFilePath, 'w') as env_file:
        envData = {
            "LANGUAGE": lang_choice,
            "TOKEN": token
        }
        json.dump(envData, env_file, indent=4)

lang = main_lang

if not os.path.exists(badWordFilePath):
    badword_data = {
        "bad_words": [
            "badword1",
            "badword2",
            "badword3"
        ]
    }
    with open(badWordFilePath, 'w') as badword_file:
        json.dump(badword_data, badword_file, indent=4)

if not os.path.exists(configFilePath):
    with open(configFilePath, 'w') as config_file:
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
        json.dump(config_data, config_file, indent=4)

try:
    with open(configFilePath, 'r') as config_file:
        config = json.load(config_file)
except Exception as e:
    print(lang.get("ERROR_CONFIG_LOAD").format(e))
    exit()

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
        botName = bot.user.name + "#" + bot.user.discriminator

    async with aiohttp.ClientSession() as session:
        async with session.get(onlineVersion) as response:
            if response.status == 200:
                botRepoVersion = await response.text()
            else:
                botRepoVersion = "Unknown"

    with open(localVersionFilePath, 'r') as version_file:
        botVersion = version_file.read().strip()

    if botVersion != botRepoVersion:
        print('='*multiplicator)
        print(lang.get("HEADER_OUTDATED_LN1"))
        print(lang.get("HEADER_OUTDATED_LN2"))
        print(lang.get("HEADER_OUTDATED_LN3"))
    print('='*multiplicator)
    print(lang.get("HEADER_LN1"))
    print(lang.get("HEADER_LN2").format(botName=botName, botId=bot.user.id))
    print(lang.get("HEADER_LN3").format(amount=len(bot.guilds)))
    print(lang.get("HEADER_LN4").format(language=botLang))
    print(lang.get("HEADER_LN5").format(prefix=prefix))
    print(lang.get("HEADER_LN6").format(owner=bot.get_user(config["YOUR_ID"])))
    print(lang.get("HEADER_LN7").format(gitBranch=gitBranch))
    print(lang.get("HEADER_LN8").format(botVersion=botVersion))
    print(lang.get("HEADER_LN9").format(botRepoVersion=botRepoVersion))
    print(lang.get("HEADER_LN10").format(apiVersion=disnake.__version__))
    print(lang.get("HEADER_LN11").format(platformSystem=platform.system(), platformVersion=platform.release(), osName=os.name))
    print(lang.get("HEADER_LN12").format(pythonVersion=platform.python_version()))
    print(lang.get("HEADER_LN13").format(timeNow=datetime.datetime.now()))
    print('='*multiplicator)

if utilsLoad:
    for files in utilsCogPath.values():
        try:
            bot.load_extension(files)
        except Exception as e:
            print(lang.get("ERROR_COG_LOADING").format(cogName=files, e=e))

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
                        print(lang.get("ERROR_COG_LOADING").format(cogName=cog_name, e=e))
    except Exception as e:
        print(lang.get("ERROR_ELEMENTS_LOADING").format(element, e))

try:
    bot.run(load_enviroment_token())
except Exception as e:
    print(lang.get("ERROR_BOT_RUN"))
    exit()
