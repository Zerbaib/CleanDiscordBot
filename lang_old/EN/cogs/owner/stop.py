from disnake.ext import commands

from lang.en.utils import error


class StopCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /stop has been loaded')

    @commands.slash_command(name="stop", description="Stop the bot")
    @commands.is_owner()
    async def stop(self, ctx):
        try:
            await ctx.send("🛑 Stopping the bot... 🛑", ephemeral=True)
            await self.bot.close()
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(StopCommand(bot))
