import disnake
from disnake.ext import commands
from termcolor import colored
import time
import datetime

class LoggerUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🧰 Logger has been loaded')
        print()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:  # Ignore messages from bots
            channel = message.channel
            user = message.author
            content = message.content

            current_time = datetime.datetime.utcnow()
            time_str = current_time.strftime("%d/%m/%Y, %H:%M:%S")

            # Color the parts of the log_message
            log_printed_message = f"UTC - {time_str} > #{colored(channel, 'green')} >>> @{colored(user, 'blue')} >> {content}"
            log_message = f"UTC - {time_str} > #{channel} - <#{channel.id}> >>> @{user} - <@{user.id}> >> {content}"
            print(log_printed_message)
            
            with open('log.txt', 'a') as log_file:
                log_file.write(log_message + '\n')

def setup(bot):
    bot.add_cog(LoggerUtils(bot))
