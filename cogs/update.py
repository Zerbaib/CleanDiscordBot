import disnake
from disnake.ext import commands
import platform
import json
import subprocess
import sys

class updateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /update as been loaded')

    @commands.slash_command(name="update", description="Get the lasted update of the bot",)
    @commands.has_permissions(administrator=True)
    async def update(self, ctx):
        with open("config.json", 'r') as config_file:
            config = json.load(config_file)
        try:
            embed = disnake.Embed(
                title=f"Update of ``{self.bot.user.name}``",
                description=f"Please wait ...",
                color=disnake.Color.random()
            )
            await ctx.response.send_message(embed=embed)

        except Exception as e:
            embed = disnake.Embed(
                title=f"Error during the ``/update``",
                description=f"```{e}```",
                color=disnake.Color.red()
                )
            embed.set_footer(text=f'Command executed by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(updateCommand(bot))