import disnake
from disnake.ext import commands
import requests
import platform

class BotInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /botinfo has been loaded')
    
    @commands.slash_command(name="botinfo", description="Get the bot's info")
    async def botinfo(self, ctx):
        try:
            with open('version.txt', 'r') as version_file:
                bot_version = version_file.read().strip()
            
            github_repo = "https://github.com/Zerbaib/CleanDiscordBot"
            online_version_url = "https://raw.githubusercontent.com/Zerbaib/CleanDiscordBot/main/version.txt"
            github_api_url = "https://api.github.com/repos/Zerbaib/CleanDiscordBot"
            
            response = requests.get(online_version_url)
            if response.status_code == 200:
                online_version = response.text.strip()
            else:
                online_version = "Unknown"

            response = requests.get(f"{github_api_url}/commits?per_page=100&sha=main")
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
            
            response = requests.get(f"{github_api_url}/stargazers")
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
                title=f"Info of ``{self.bot.user.name}``",
                color=disnake.Color.old_blurple()
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
                value=f"**Bot version**: ``{bot_version}``\n"
                      f"**API version**: ``{disnake.__version__}``\n"
                      f"**Python version**: ``{platform.python_version()}``",
                inline=False
            )
            embed.add_field(
                name=f"__GitHub Repository:__",
                value=f"**Commits**: ``{commit_count}``\n"
                      f"**Stars**: ``{stargazer_count}``\n"
                      f"**Online Version**: ``{online_version}``",
                inline=False
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(text=f'Command executed by {ctx.author}', icon_url=ctx.author.avatar.url)
            
            await ctx.response.send_message(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title=f"Error during the ``/botinfo``",
                description=f"```{e}```",
                color=disnake.Color.red()
            )
            embed.set_footer(text=f'Command executed by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(BotInfoCommand(bot))
