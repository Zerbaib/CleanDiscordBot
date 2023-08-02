import disnake
from disnake.ext import commands
from termcolor import colored  # Import colored from the termcolor library

class Logger(commands.Cog):
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

            # Color the parts of the log_message
            log_printed_message = f"#{colored(channel, 'green')} >>> @{colored(user, 'blue')} >> {content}"
            log_message = f"#{channel} >>> @{user} >> {content}"
            print(log_printed_message)  # You can replace this with your desired logging mechanism
            
            with open('log.txt', 'a') as log_file:
                log_file.write(log_message + '\n')

def setup(bot):
    bot.add_cog(Logger(bot))
