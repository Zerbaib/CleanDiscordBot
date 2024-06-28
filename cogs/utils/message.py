import datetime
import disnake
from disnake.ext import commands
from termcolor import colored

from utils.logger import printLog

class onMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🧰 On Message has been loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        user = message.author
        content = message.content
        currentTime = datetime.datetime.utcnow()
        timeStr = currentTime.strftime("%d/%m/%Y, %H:%M:%S")
        
        if message.attachments:
            for attachment in message.attachments:
                content += f" | more content: {attachment.url}"
        elif message.embeds:
            for embed in message.embeds:
                content += f" | more content: {embed.url}"
        
        log_printed_message = f"UTC - {timeStr} > #{colored(channel, 'green')} >>> @{colored(user, 'blue')} >> {content}"
        
        printLog(f"UTC - {timeStr} > #{colored(channel, 'green')} >>> @{colored(user, 'blue')} >> {content}")
        return

def setup(bot):
    bot.add_cog(onMessageCog(bot))