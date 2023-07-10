import disnake
from disnake.ext import commands
import os
import json
import subprocess
import sys

class updateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /update has been loaded')

    @commands.slash_command(name="update", description="Get the latest update of the bot")
    @commands.is_owner()
    async def update(self, ctx):
        with open("config.json", 'r') as config_file:
            config = json.load(config_file)
        try:
            embed = disnake.Embed(
                title=f"Update of ``{self.bot.user.name}``",
                description=f"Please wait...",
                color=disnake.Color.random()
            )
            await ctx.response.send_message(embed=embed)

            # Exécuter la commande de mise à jour du bot
            update_process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = update_process.communicate()

            # Vérifier si la mise à jour a réussi
            if update_process.returncode == 0:
                embed.title = f"Update of ``{self.bot.user.name}``"
                embed.description = "Update successful! Restarting the bot..."
                await ctx.followup.send(embed=embed)

                # Redémarrer le bot
                python = sys.executable
                os.execl(python, python, *sys.argv)
            else:
                error_message = stderr.decode("utf-8")
                embed.title = f"Error during the ``/update``"
                embed.description = f"```{error_message}```"
                embed.color = disnake.Color.red()
                await ctx.followup.send(embed=embed)

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
