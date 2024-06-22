import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import other_lang as langText



class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /ping has been loaded')

    @commands.slash_command(name="ping", description=langText.get("PING_DESCRIPTION"))
    async def ping(self, ctx):
        try:
            embed = disnake.Embed(
                title=langText.get("PING_TITLE"),
                description=langText.get("PING_TEXT").format(latency=round(self.bot.latency * 1000)),
                color=disnake.Color.blurple()
                )
            embed.set_footer(text=langText.get("PING_FOOTER").format(author=ctx.author), icon_url=ctx.author.avatar.url)
            await ctx.response.defer()
            await ctx.send(ephemeral=True, embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(PingCommand(bot))