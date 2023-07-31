import disnake
from disnake.ext import commands
import requests
import platform
from utils import error

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github_repo = "https://github.com/Zerbaib/CleanDiscordBot"
        self.online_version_url = "https://raw.githubusercontent.com/Zerbaib/CleanDiscordBot/main/version.txt"
        self.github_api_url = "https://api.github.com/repos/Zerbaib/CleanDiscordBot"

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ Info ⚙️ ==========')
        print('🔩 /botinfo has been loaded')
        print('🔩 /userinfo has been loaded')
        print('🔩 /serverinfo has been loaded')
        print()
    
    @commands.slash_command(name="botinfo", description="Get the bot's info")
    async def botinfo(self, ctx):
        try:
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
                      f"**Online Version**: ``{online_version}\n``"
                      f"**Repo link**: [**`here`**]({self.github_repo})",
                inline=False
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(text=f'Command executed by {ctx.author}', icon_url=ctx.author.avatar.url)
            
            # await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="userinfo", description="Get user information")
    async def userinfo(self, ctx, user: disnake.User = None):
        try:
            time = "%H:%M:%S %Y-%m-%d"
            if user is None:
                user = ctx.author

            embed = disnake.Embed(
                title="User Information",
                color=disnake.Color.blue()
            )
            
            if user.avatar:
                embed.set_thumbnail(url=user.avatar.url)
            else:
                embed.set_thumbnail(url=user.default_avatar.url)
            
            embed.add_field(name="Username", value=f"```{user.name}```", inline=True)
            
            if user.discriminator != '0':
                embed.add_field(name="Discriminator", value=f"```{user.discriminator}```", inline=True)
            else:
                embed.add_field(name="Display Name", value=f"```{user.display_name}```", inline=True)
            
            embed.add_field(name="ID", value=f"```{user.id}```", inline=False)
            embed.add_field(name="Bot", value=f"```{user.bot}```", inline=True)
            embed.add_field(name="Created At", value=f"```{user.created_at.strftime(time)}```", inline=True)

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="serverinfo", description="Display server information")
    async def serverinfo(self, ctx):
        try:
            guild = ctx.guild

            name = guild.name
            logo = guild.icon.url if guild.icon else None
            description = guild.description
            owner = guild.owner
            created_at = guild.created_at
            member_count = guild.member_count
            channel_count = len(guild.channels)
            role_count = len(guild.roles)
            boost_count = guild.premium_subscription_count
            boost_tier = guild.premium_tier
            date = "%d-%m-%Y %H:%M:%S"

            embed = disnake.Embed(title="Server Information", color=disnake.Color.blurple())
            if logo:
                embed.set_thumbnail(url=logo)
            embed.add_field(name="Name", value=f"```{name}```", inline=False)
            if description:
                embed.add_field(name="Description", value=f"```{description}```", inline=False)
            embed.add_field(name="Owner", value=f"{owner.mention}", inline=False)
            embed.add_field(name="Created At", value=f"```{created_at.strftime(date)}```", inline=False)
            embed.add_field(name="Member Count", value=f"```{str(member_count)}```", inline=True)
            embed.add_field(name="Channel Count", value=f"```{str(channel_count)}```", inline=True)
            embed.add_field(name="Role Count", value=f"```{str(role_count)}```", inline=True)
            embed.add_field(name="Boost Count", value=f"```{str(boost_count)}```", inline=True)
            embed.add_field(name="Boost Tier", value=f"```{str(boost_tier)}```", inline=True)

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(InfoCog(bot))
