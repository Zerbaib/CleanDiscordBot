import disnake
from disnake.ext import commands
import subprocess
import sys

class RestartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /restart has been loaded')

    @commands.slash_command(name="restart", description="Restart the bot")
    @commands.is_owner()  # Exige que l'auteur de la commande soit le propriétaire du bot
    async def restart(self, ctx):
        try:
            embed = disnake.Embed(
                title="Restarting...",
                description="The bot is restarting. Please wait...",
                color=disnake.Color.random()
            )
            await ctx.response.send_message(embed=embed)

            # Exécuter une nouvelle instance du script bot
            python = sys.executable
            subprocess.Popen([python, "main.py"])

            # Terminer le processus actuel du bot
            sys.exit()

        except Exception as e:
            embed = disnake.Embed(
                title="Error during restart",
                description=f"```{e}```",
                color=disnake.Color.red()
            )
            await ctx.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(RestartCog(bot))
