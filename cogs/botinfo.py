import disnake
from disnake.ext import commands

class botinfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /botinfo as been loaded')
    
    @commands.slash_command(name="botinfo", description="Get the bot's info",)
    async def botinfo(self, ctx):
        try:
            embed = disnake.Embed(
                title=f"Info of {self.bot.name}",
                description=f"The ping is around `{round(self.bot.latency * 1000)}ms`",
                color=disnake.Color.random()
                )
            embed.set_footer(text=f'Command executed by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.response.send_message(ephemeral=True, embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title=f"Error during the ``/ping``",
                description=f"```{e}```",
                color=disnake.Color.red()
                )
            embed.set_footer(text=f'Command executed by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(botinfoCommand(bot))