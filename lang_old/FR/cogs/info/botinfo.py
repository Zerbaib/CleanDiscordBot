import platform

import disnake
import requests
from disnake.ext import commands

from lang.fr.utils import error


class BotinfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github_repo = "https://github.com/Zerbaib/CleanDiscordBot"
        self.online_version_url = "https://raw.githubusercontent.com/Zerbaib/CleanDiscordBot/main/version.txt"
        self.github_api_url = "https://api.github.com/repos/Zerbaib/CleanDiscordBot"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /botinfo has been loaded')

    @commands.slash_command(name="botinfo", description="Optient les informations du bot")
    async def botinfo(self, ctx):
        try:
            
            await ctx.response.defer()
            
            with open('version.txt', 'r') as version_file:
                bot_version = version_file.read().strip()
            
            response = requests.get(self.online_version_url)
            if response.status_code == 200:
                online_version = response.text.strip()
            else:
                online_version = "Unknown"

            response = requests.get(f"{self.github_api_url}/commits?per_page=100&sha=main")
            if response.status_code == 200:
                commits = response.json()
                commit_count = len(commits)
                while "Link" in response.headers and "rel=\"next\"" in response.headers["Link"]:
                    next_page_url = response.headers["Link"].split(";")[0][1:-1]
                    response = requests.get(next_page_url)
                    if response.status_code == 200:
                        commits += response.json()
                        commit_count += len(response.json())
            else:
                commit_count = "Unknown"
            
            response = requests.get(f"{self.github_api_url}/stargazers")
            if response.status_code == 200:
                stargazers = response.json()
                stargazer_count = len(stargazers)
                while "Link" in response.headers and "rel=\"next\"" in response.headers["Link"]:
                    next_page_url = response.headers["Link"].split(";")[0][1:-1]
                    response = requests.get(next_page_url)
                    if response.status_code == 200:
                        stargazers += response.json()
                        stargazer_count += len(response.json())
            else:
                stargazer_count = "Unknown"

            embed = disnake.Embed(
                title=f"Info de ``{self.bot.user.name}`` 🤖",
                color=disnake.Color.old_blurple()
            )
            embed.add_field(
                name=f"__Profile du Bot:__",
                value=f"**Prénom**: ``{self.bot.user.name}``\n"
                      f"**Prefix**: ``{self.bot.command_prefix}``\n"
                      f"**Latence**: ``{round(self.bot.latency * 1000)}ms``",
                inline=False
            )
            embed.add_field(
                name=f"__Info du Bot:__",
                value=f"**Version du Bot**: ``{bot_version}``\n"
                      f"**Version de l'API**: ``{disnake.__version__}``\n"
                      f"**Version de Python**: ``{platform.python_version()}``",
                inline=False
            )
            embed.add_field(
                name=f"__GitHub Repository:__",
                value=f"**Commits**: ``{commit_count}``\n"
                      f"**Stars**: ``{stargazer_count}``\n"
                      f"**Version en Ligne**: ``{online_version}\n``"
                      f"**Repo link**: [**`here`**]({self.github_repo})",
                inline=False
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(text=f'Commandes demander par {ctx.author}', icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(BotinfoCommand(bot))