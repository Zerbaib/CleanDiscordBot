import disnake
from disnake.ext import commands
import json
import requests

class UpdateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /check has been loaded')

    @commands.slash_command(name="check", description="Check if the bot is up to date")
    @commands.is_owner()
    async def check(self, ctx):
        try:
            online_version_url = "https://raw.githubusercontent.com/Zerbaib/CleanDiscordBot/main/version.txt"
            response = requests.get(online_version_url)
            if response.status_code == 200:
                online_version = response.text.strip()
                local_version = self.get_local_version()  # Méthode pour obtenir la version locale

                embed = disnake.Embed(
                    title=f"Check of {self.bot.user.name}",
                    color=disnake.Color.random()
                )
                if online_version == local_version:
                    embed.description = "The bot is up to date."
                else:
                    embed.description = "An update is available."

                embed.add_field(name="Local Version", value=f"```{local_version}```", inline=True)
                embed.add_field(name="Online Version", value=f"```{online_version}```", inline=True)
                await ctx.response.send_message(embed=embed)

        except Exception as e:
            embed = disnake.Embed(
                title=f"Error during the `/check`",
                description=f"```{e}```",
                color=disnake.Color.red()
            )
            embed.set_footer(text=f'Command executed by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.response.send_message(embed=embed)

    def get_local_version(self):
        with open("version.txt", "r") as version_file:
            local_version = version_file.read().strip()
        return local_version

def setup(bot):
    bot.add_cog(UpdateCommand(bot))
