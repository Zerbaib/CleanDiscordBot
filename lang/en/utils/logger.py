import datetime
import json
import time
import disnake
from disnake.ext import commands
from termcolor import colored

def log_writer(time_str, channel, user, content):
    log_message = f"UTC - {time_str} > #{channel} - <#{channel.id}> >>> @{user} - <@{user.id}> >> {content}"

    with open('log.txt', 'a', encoding='utf-8') as log_file:  # Specify 'utf-8' encoding
        log_file.write(log_message + '\n')

class LoggerUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🧰 Logger has been loaded')
        print()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)

            channel = message.channel
            user = message.author
            content = message.content
            current_time = datetime.datetime.utcnow()
            time_str = current_time.strftime("%d/%m/%Y, %H:%M:%S")

            log_printed_message = f"UTC - {time_str} > #{colored(channel, 'green')} >>> @{colored(user, 'blue')} >> {content}"
            print(log_printed_message)

            log_channel_id = config["LOG_ID"]
            log_channel = self.bot.get_channel(log_channel_id)

            # Create and send the embed
            embed = disnake.Embed(
                title=f"{user.display_name}",
                description=f"``UTC - {time_str}``\nUser has posted a message\n",
                color=disnake.Color.blurple()
            )
            embed.add_field(
                name="Channel",
                value=f"<#{channel.id}>",
                inline=True
            )
            embed.add_field(
                name="User",
                value=f"<@{user.id}>",
                inline=True
            )
            embed.add_field(
                name="Message Content",
                value=f"```{content}```",
                inline=False
            )
            await log_channel.send(embed=embed)
            log_writer(time_str, channel, user, content)

def setup(bot):
    bot.add_cog(LoggerUtils(bot))
