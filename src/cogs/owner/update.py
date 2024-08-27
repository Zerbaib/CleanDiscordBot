import json
import subprocess

import disnake
from disnake.ext import commands
from utils import error
from utils.load_lang import owner_lang as langText
from modules.var import *



class UpdateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /update has been loaded')

    @commands.slash_command(name="update", description="Get the latest update of the bot")
    @commands.is_owner()
    async def update(self, ctx):
        try:
            with open(folders.config, 'r') as config_file:
                config = json.load(config_file)

            embed = disnake.Embed(
                title=f"⤴️ Update of ``{self.bot.user.name}``",
                description=f"Please wait...",
                color=disnake.Color.old_blurple()
            )
            await ctx.send(embed=embed)

            update_process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = update_process.communicate()

            if update_process.returncode == 0:
                success_embed = disnake.Embed(
                    title=f"⤴️ Update of ``{self.bot.user.name}``",
                    description="✅ Update successful!\nYou just need a restart to apply the update.",
                    color=disnake.Color.brand_green()
                )
                await ctx.send(embed=success_embed)
            else:
                error_message = stderr.decode("utf-8")
                error_embed = disnake.Embed(
                    title=f"↩️ Error during the ``/update``",
                    description=f"```{error_message}```",
                    color=disnake.Color.brand_red()
                )
                await ctx.send(embed=error_embed)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UpdateCommand(bot))