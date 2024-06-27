import disnake
from disnake.ext import commands

class onMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🧰 On Message has been loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        return

def setup(bot):
    bot.add_cog(onMessageCog(bot))