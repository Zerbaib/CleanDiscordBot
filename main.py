import disnake
from disnake.ext import commands
import json
import os
import platform

config_file_path = "config.json"

if not os.path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        token = input("Enter the bot's token:\n")
        prefix = input("Enter the bot's prefix:\n")
        log_id = int(input("Enter the log's channel ID:\n"))
        id_client = int(input("Enter your Discord ID:\n"))
        config_data = {
            "TOKEN": token,
            "PREFIX": prefix,
            "LOG_ID": log_id,
            "YOUR_ID": id_client,
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

@bot.event
async def on_ready():
    if bot.user.discriminator == 0:
        nbot = bot.user.name
    else:
        nbot = bot.user.name + "#" + bot.user.discriminator

    print('===============================================')
    print(f"🔱 The bot is ready!")
    print(f'🔱 Logged in as {nbot} | {bot.user.id}')
    print(f"🔱 Disnake version: {disnake.__version__}")
    print(f"🔱 Running on {platform.system()} {platform.release()} {os.name}")
    print(f"🔱 Python version: {platform.python_version()}")
    print('===============================================')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cog_name = filename[:-3]
        try:
            bot.load_extension(f'cogs.{cog_name}')
        except Exception as e:
            print(f"🌪️  Erreur dans le chargement de l'extension '{cog_name}': {e}")

bot.run(token)