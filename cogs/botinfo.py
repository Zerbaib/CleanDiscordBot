import disnake
from disnake.ext import commands
import platform

class botinfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /botinfo as been loaded')
    
    @commands.slash_command(name="botinfo", description="Get the bot's info",)
    async def botinfo(self, ctx):
        try:
            with open('version.txt', 'r') as version_file:
                bot_version = version_file.read().strip()
            embed = disnake.Embed(
                title=f"Info of ``{self.bot.user.name}``",
                description=f"",
                color=disnake.Color.random()
                )
            embed.add_field(
                name=f"__Bot profile:__",
                value=f"**Name**: ``{self.bot.user.name}``\n"
                      f"**Prefix**: ``{self.bot.command_prefix}``\n"
                      f"**Ping**: ``{round(self.bot.latency * 1000)}ms``",
                inline=False
            )
            embed.add_field(
                name=f"__Bot info:__",
                value=f"**Version**: ``{bot_version}``\n"
                      f"**Api version**: ``{disnake.__version__}``\n"
                      f"**Python version**: ``{platform.python_version()}``",
                inline=False
            )
            embed.set_footer(text=f'Command executed by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.response.send_message(ephemeral=True, embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title=f"Error during the ``/botinfo``",
                description=f"```{e}```",
                color=disnake.Color.red()
                )
            embed.set_footer(text=f'Command executed by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(botinfoCommand(bot))