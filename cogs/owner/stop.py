from disnake.ext import commands

from utils import error
from utils.load_lang import load_owner_lang

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
