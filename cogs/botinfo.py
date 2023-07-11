import disnake
from disnake.ext import commands
import platform
import requests

class botinfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /botinfo has been loaded')
    
    @commands.slash_command(name="botinfo", description="Get the bot's info")
    async def botinfo(self, ctx):
        try:
            with open('version.txt', 'r') as version_file:
                bot_version = version_file.read().strip()
            
            github_repo = "https://github.com/Zerbaib/CleanDiscordBot"
            online_version_url = "https://raw.githubusercontent.com/Zerbaib/CleanDiscordBot/main/version.txt"
            
            response = requests.get(online_version_url)
            if response.status_code == 200:
                online_version = response.text.strip()
            else:
                online_version = "Unknown"

            response = requests.get(f'{github_repo}/commits')
            commit_count = len(response.json()) if response.status_code == 200 else "Unknown"
            
            response = requests.get(f'{github_repo}/stargazers')
            stargazer_count = len(response.json()) if response.status_code == 200 else "Unknown"

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
            embed.add_field(
                name=f"__GitHub Repository:__",
                value=f"**Commits**: ``{commit_count}``\n"
                      f"**Stars**: ``{stargazer_count}``\n"
                      f"**Version**: ``{online_version}``",
                inline=False
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
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
