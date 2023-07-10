import disnake
from disnake.ext import commands
import os
import requests

class updater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 updater as been loaded')

def setup(bot):
    bot.add_cog(updater(bot))