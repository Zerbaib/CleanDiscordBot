import platform

import disnake
import requests
from disnake.ext import commands

from lang.fr.utils import error


class UserinfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github_repo = "https://github.com/Zerbaib/CleanDiscordBot"
        self.online_version_url = "https://raw.githubusercontent.com/Zerbaib/CleanDiscordBot/main/version.txt"
        self.github_api_url = "https://api.github.com/repos/Zerbaib/CleanDiscordBot"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /userinfo has been loaded')

    @commands.slash_command(name="userinfo", description="Optient les informations d'un utilisateur")
    async def userinfo(self, ctx, user: disnake.User = None):
        try:
            time = "%H:%M:%S %Y-%m-%d"
            if user is None:
                user = ctx.author

            embed = disnake.Embed(
                title="```👤 User Information 👤```",
                color=disnake.Color.blue()
            )
            
            if user.avatar:
                embed.set_thumbnail(url=user.avatar.url)
            else:
                embed.set_thumbnail(url=user.default_avatar.url)
            
            embed.add_field(name="```Pseudo```", value=f"```{user.name}```", inline=True)
            
            if user.discriminator != '0':
                embed.add_field(name="```Discriminateur```", value=f"```{user.discriminator}```", inline=True)
            else:
                embed.add_field(name="```Pseudo Afficher```", value=f"```{user.display_name}```", inline=True)
            
            embed.add_field(name="```ID```", value=f"```{user.id}```", inline=False)
            embed.add_field(name="```Bot```", value=f"```{user.bot}```", inline=True)
            embed.add_field(name="```Crée le```", value=f"```{user.created_at.strftime(time)}```", inline=True)

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserinfoCommand(bot))