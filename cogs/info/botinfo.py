import platform

import disnake
import requests
from disnake.ext import commands

from utils import error
from utils.load_lang import info_lang

langText = info_lang


class BotInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github_repo = "https://github.com/Zerbaib/CleanDiscordBot"
        self.online_version_url = "https://raw.githubusercontent.com/Zerbaib/CleanDiscordBot/main/version.txt"
        self.github_api_url = "https://api.github.com/repos/Zerbaib/CleanDiscordBot"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /botinfo has been loaded')
    
    @commands.slash_command(name="botinfo", description=langText.get("BOTINFO_DESCRIPTION"))
    async def botinfo(self, ctx):
        try:
            await ctx.response.defer()
            
            with open('version.txt', 'r') as version_file:
                bot_version = version_file.read().strip()
            
            response = requests.get(self.online_version_url)
            if response.status_code == 200:
                online_version = response.text.strip()
            else:
                online_version = langText.get("UNKNOWN")

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
                commit_count = langText.get("UNKNOWN")
            
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
                stargazer_count = langText.get("UNKNOWN")

            embed = disnake.Embed(
                title=langText.get("BOTINFO_TITLE").format(b=self.bot.user.name),
                color=disnake.Color.old_blurple()
            )
            embed.add_field(
                name=langText.get("BOTINFO_BOTPROFILE_TITLE"),
                value=langText.get("BOTINFO_BOTPROFILE_TEXT").format(botName=self.bot.user.name, botPrefix=self.bot.command_prefix, botPing=round(self.bot.latency * 1000)),
                inline=False
            )
            embed.add_field(
                name=langText.get("BOTINFO_BOTINFO_TITLE"),
                value=langText.get("BOTINFO_BOTINFO_TEXT").format(botVer=bot_version, apiVer=disnake.__version__, pyVer=platform.python_version()),
                inline=False
            )
            embed.add_field(
                name=langText.get("BOTINFO_GITINFO_TITLE"),
                value=langText.get("BOTINFO_GITINFO_TEXT").format(commits=commit_count, stars=stargazer_count, onVer=online_version, repoLink=self.github_repo),
                inline=False
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(text=langText.get("BOTINFO_FOOTER").format(author=ctx.author), icon_url=ctx.author.avatar.url)
            
            # await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BotInfoCommand(bot))
