import subprocess
import sys

import disnake
from disnake.ext import commands

from cogs.utils import error
from cogs.utils.color import hex_to_discord_color
from cogs.utils.embed import create_embed
from cogs.utils.lang_loader import load_owner_lang

langText = load_owner_lang()


class RestartCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /restart has been loaded')

    @commands.slash_command(name="restart", description="Restart the bot")
    @commands.is_owner()
    async def restart(self, ctx):
        try:
            embed = disnake.Embed(
                title="🔄 Restarting... 🔄",
                description="The bot is restarting. Please wait...",
                color=disnake.Color.blurple()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed)

            python = sys.executable
            subprocess.Popen([python, "main.py"])

            sys.exit()

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(RestartCommand(bot))
