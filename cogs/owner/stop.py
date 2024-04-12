from disnake.ext import commands

from cogs.utils import error
from cogs.utils.color import hex_to_discord_color
from cogs.utils.embed import create_embed
from cogs.utils.lang_loader import load_owner_lang

langText = load_owner_lang()


class StopCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /stop has been loaded')

    @commands.slash_command(name="stop", description=langText.get("STOP_DESCRIPTION"))
    @commands.is_owner()
    async def stop(self, ctx):
        try:
            await ctx.send(langText.get("STOP_TITLE"), ephemeral=True)
            await self.bot.close()
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(StopCommand(bot))
