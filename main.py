import os
import json
import platform
import requests
import disnake
from disnake.ext import commands
from utils import status

config_file_path = "config.json"
casino_data_file_path = "data/casino.json"
rank_data_file_path = "data/rank.json"
casino_cooldown_data_file_path = "data/cooldown.json"
online_version = "https://raw.githubusercontent.com/Zerbaib/CleanDiscordBot/main/version.txt"

if not os.path.exists(casino_data_file_path):
    with open(casino_data_file_path, 'w') as casino_file:
        json.dump({}, casino_file)
if not os.path.exists(casino_cooldown_data_file_path):
    with open(casino_cooldown_data_file_path, 'w') as casino_cooldown_file:
        json.dump({}, casino_cooldown_file)
if not os.path.exists(rank_data_file_path):
    with open(rank_data_file_path, 'w') as rank_file:
        json.dump({}, rank_file)

if not os.path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        token = input("Enter the bot's token:\n")
        prefix = input("Enter the bot's prefix:\n")
        log_id = int(input("Enter the log's channel ID:\n"))
        poll_id = int(input("Enter the pull's channel ID:\n"))
        voice_id = int(input("Enter the voice's channel ID\nUsed for create salon on join:\n"))
        id_client = int(input("Enter your Discord ID:\n"))
        mute_id = int(input("Enter role id of muted role:\n"))
        config_data = {
            "TOKEN": token,
            "PREFIX": prefix,
            "LOG_ID": log_id,
            "POLL_ID": poll_id,
            "AUTO_VOICE_ID": voice_id,
            "YOUR_ID": id_client,
            "MUTE_ROLE_ID": mute_id,
            "del_time": 3
        }
        json.dump(config_data, config_file, indent=4)
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
else:
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)

token = config["TOKEN"]
prefix = config["PREFIX"]

bot = commands.Bot(
    command_prefix=prefix,
    intents=disnake.Intents.all(),
    case_insensitive=True
)
bot.remove_command('help')

@bot.event
async def on_ready():
    if bot.user.discriminator == 0:
        nbot = bot.user.name
    else:
        nbot = bot.user.name + "#" + bot.user.discriminator

    response = requests.get(online_version)
    if response.status_code == 200:
        bot_repo_version = response.text.strip()
    else:
        bot_repo_version = "Unknown"

    with open('version.txt', 'r') as version_file:
        bot_version = version_file.read().strip()

    if bot_version != bot_repo_version:
        print()
        print('===============================================')
        print('🛑 You are not using the latest version!')
        print('🛑 Please update the bot.')
        print('🛑 Use "git fetch && git pull" to update your bot.')
    print('===============================================')    
    print(f"🔱 The bot is ready!")
    print(f'🔱 Logged in as {nbot} | {bot.user.id}')
    print(f'🔱 Bot local version: {bot_version}')
    print(f'🔱 Bot online version: {bot_repo_version}')
    print(f"🔱 Disnake version: {disnake.__version__}")
    print(f"🔱 Running on {platform.system()} {platform.release()} {os.name}")
    print(f"🔱 Python version: {platform.python_version()}")
    print('===============================================')
    bot.loop.create_task(status.update_status(bot))

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        cog_name = filename[:-3]
        try:
            bot.load_extension(f'cogs.{cog_name}')
        except Exception as e:
            print(f"🌪️  Erreur dans le chargement de l'extension '{cog_name}':\n\n{e}")

bot.run(token)