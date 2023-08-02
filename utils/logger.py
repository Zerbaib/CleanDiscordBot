import disnake
from disnake.ext import commands
from termcolor import colored
import time
import datetime
import json

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
            log_message = f"UTC - {time_str} > #{channel} - <#{channel.id}> >>> @{user} - <@{user.id}> >> {content}"
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

            with open('log.txt', 'a') as log_file:
                log_file.write(log_message + '\n')

def setup(bot):
    bot.add_cog(LoggerUtils(bot))
