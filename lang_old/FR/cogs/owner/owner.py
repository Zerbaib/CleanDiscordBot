import json
import os
import subprocess
import sys

import disnake
import requests
from disnake.ext import commands

from lang.fr.utils import error


class OwnerCommands(commands.Cog):
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


    @commands.slash_command(name="check", description="Regarde si une mise à jour est disponible")
    @commands.is_owner()
    async def check(self, ctx):
        try:
            
            response = requests.get(self.online_version_url)
            if response.status_code == 200:
                online_version = response.text.strip()
                local_version = self.get_local_version()  # Méthode pour obtenir la version locale

                embed = disnake.Embed(
                    title=f"🔎 Verifiquation de {self.bot.user.name}",
                )
                if online_version == local_version:
                    embed.description = "Le bot est a jour. 👍"
                    embed.colour = disnake.Color.brand_green()
                else:
                    embed.description = "Une mise a jour est disponible. 👎"
                    embed.colour = disnake.Color.brand_red()

                embed.add_field(name="Version Local", value=f"```{local_version}```", inline=True)
                embed.add_field(name="Version En Ligne", value=f"```{online_version}```", inline=True)
                await ctx.response.defer()
                await ctx.send(embed=embed)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="update", description="Optien la dernière version du bot")
    @commands.is_owner()
    async def update(self, ctx):
        try:
            with open("config.json", 'r') as config_file:
                config = json.load(config_file)
            
            embed = disnake.Embed(
                title=f"⤴️ Mise a jour de ``{self.bot.user.name}``",
                description=f"Merci de patienter pendant que je met a jour le bot. ⏳",
                color=disnake.Color.old_blurple()
            )
            await ctx.send(embed=embed)

            # Exécuter la commande de mise à jour du bot
            update_process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = update_process.communicate()

            # Vérifier si la mise à jour a réussi
            if update_process.returncode == 0:
                success_embed = disnake.Embed(
                    title=f"⤴️ Mise a jour de ``{self.bot.user.name}``",
                    description="✅ La mise a jours n'a pas eu de probleme.\nIl est recommandé de redémarrer le bot.",
                    color=disnake.Color.brand_green()
                )
                await ctx.send(embed=success_embed)
            else:
                error_message = stderr.decode("utf-8")
                error_embed = disnake.Embed(
                    title=f"↩️ Une erreur c'est produite durant le ``/update``",
                    description=f"```{error_message}```",
                    color=disnake.Color.brand_red()
                )
                await ctx.send(embed=error_embed)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)


    @commands.slash_command(name="restart", description="Redémarre le bot")
    @commands.is_owner()
    async def restart(self, ctx):
        try:
            embed = disnake.Embed(
                title="🔄 Redémarage ... 🔄",
                description="Le bot va redémarrer ...",
                color=disnake.Color.old_blurple()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed)

            python = sys.executable
            subprocess.Popen([python, "main.py"])
            sys.exit()
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="stop", description="Arrête le bot")
    @commands.is_owner()
    async def stop(self, ctx):
        try:
            await ctx.send("🛑 Arret du bot 🛑", ephemeral=True)
            await self.bot.close()
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(OwnerCommands(bot))
