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
    async def update(ctx):
        try:
            with open("config.json", 'r') as config_file:
                config = json.load(config_file)
            if ctx.author.id == config["YOUR_ID"]:
                if platform.system() == "Windows":
                    try:
                        embed = disnake.Embed(
                            title="Updating... (Windows)",
                            description="Updating the bot from the Github Repo...",
                            color=disnake.Color.random()
                            )
                        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                        subprocess.call('cls')
                        subprocess.call("git fetch", shell=True)
                        subprocess.call("git pull", shell=True)
                        subprocess.call([sys.executable, "main.py"])
                        sys.exit()
                    except:
                        await ctx.send("Git failed to update the bot! Please try again later.")

                elif platform.system() == "Linux":
                    try:
                        embed = disnake.Embed(
                            title="Updating... (Linux)",
                            description="Updating the bot from the Github Repo...",
                            color=disnake.Color.random()
                            )
                        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                        subprocess.call('clear')
                        subprocess.call(["git", "fetch"])
                        subprocess.call(["git", "pull"])
                        subprocess.call([sys.executable, "main.py"])
                        sys.exit()
                    except:
                        await ctx.send("Git failed to update the bot! Please try again later.")
                else:
                    embed = disnake.Embed(
                        title="Error",
                        description="Your OS is not supported!",
                        color=disnake.Color.dark_red()
                        )
                    await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Error",
                    description="You are not allowed to use this command!",
                    color=disnake.Color.dark_red()
                    )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title="Error",
                description=f"An error occured while updating the bot! {e}",
                color=disnake.Color.dark_red()
                )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(updateCommand(bot))