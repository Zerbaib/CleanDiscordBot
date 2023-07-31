import disnake
from disnake.ext import commands
import json
import requests
import subprocess
import sys
import os
from utils import error

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.online_version_url = "https://raw.githubusercontent.com/Zerbaib/CleanDiscordBot/main/version.txt"

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ Owner ⚙️ ==========')
        print('🔩 /check has been loaded')
        print('🔩 /update has been loaded')
        print('🔩 /restart has been loaded')
        print('🔩 /stop has been loaded')
        print()

    def get_local_version(self):
        with open("version.txt", "r") as version_file:
            local_version = version_file.read().strip()
        return local_version


    @commands.slash_command(name="check", description="Check if the bot is up to date")
    @commands.is_owner()
    async def check(self, ctx):
        try:
            
            response = requests.get(self.online_version_url)
            if response.status_code == 200:
                online_version = response.text.strip()
                local_version = self.get_local_version()  # Méthode pour obtenir la version locale

                embed = disnake.Embed(
                    title=f"Check of {self.bot.user.name}",
                )
                if online_version == local_version:
                    embed.description = "The bot is up to date."
                    embed.colour = disnake.Color.brand_green()
                else:
                    embed.description = "An update is available."
                    embed.colour = disnake.Color.brand_red()

                embed.add_field(name="Local Version", value=f"```{local_version}```", inline=True)
                embed.add_field(name="Online Version", value=f"```{online_version}```", inline=True)
                await ctx.response.defer()
                await ctx.send(embed=embed)

        except Exception as e:
            error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="update", description="Get the latest update of the bot")
    @commands.is_owner()
    async def update(self, ctx):
        try:
            with open("config.json", 'r') as config_file:
                config = json.load(config_file)
            embed = disnake.Embed(
                title=f"Update of ``{self.bot.user.name}``",
                description=f"Please wait...",
                color=disnake.Color.random()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed)

            # Exécuter la commande de mise à jour du bot
            update_process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = update_process.communicate()

            # Vérifier si la mise à jour a réussi
            if update_process.returncode == 0:
                embed.title = f"Update of ``{self.bot.user.name}``"
                embed.description = "Update successful! Restarting the bot..."
                await ctx.response.defer()
                await ctx.send(embed=embed)

                # Redémarrer le bot
                python = sys.executable
                os.execl(python, python, *sys.argv)
            else:
                error_message = stderr.decode("utf-8")
                embed.title = f"Error during the ``/update``"
                embed.description = f"```{error_message}```"
                embed.color = disnake.Color.red()
                await ctx.response.defer()
                await ctx.send(embed=embed)

        except Exception as e:
            error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="restart", description="Restart the bot")
    @commands.is_owner()  # Exige que l'auteur de la commande soit le propriétaire du bot
    async def restart(self, ctx):
        try:
            embed = disnake.Embed(
                title="Restarting...",
                description="The bot is restarting. Please wait...",
                color=disnake.Color.random()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed)

            # Exécuter une nouvelle instance du script bot
            python = sys.executable
            subprocess.Popen([python, "main.py"])

            # Terminer le processus actuel du bot
            sys.exit()

        except Exception as e:
            error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="stop", description="Stop the bot")
    @commands.is_owner()
    async def stop(self, ctx):
        try:
            await ctx.send("Stopping the bot...", ephemeral=True)
            await self.bot.close()
        except Exception as e:
            error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(OwnerCog(bot))
