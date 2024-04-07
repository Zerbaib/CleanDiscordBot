import platform

import disnake
import requests
from disnake.ext import commands

from lang.fr.utils import error


class ServerinfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github_repo = "https://github.com/Zerbaib/CleanDiscordBot"
        self.online_version_url = "https://raw.githubusercontent.com/Zerbaib/CleanDiscordBot/main/version.txt"
        self.github_api_url = "https://api.github.com/repos/Zerbaib/CleanDiscordBot"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /serverinfo has been loaded')

    @commands.slash_command(name="serverinfo", description="Regarde les informations du serveur")
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

            embed = disnake.Embed(title="```💾 Information du Serveur 💾```", color=disnake.Color.blurple())
            if logo:
                embed.set_thumbnail(url=logo)
            embed.add_field(name="```Nom```", value=f"```{name}```", inline=False)
            if description:
                embed.add_field(name="```Description```", value=f"```{description}```", inline=False)
            embed.add_field(name="```Proprietaire```", value=f"{owner.mention}", inline=False)
            embed.add_field(name="```Crée le```", value=f"```{created_at.strftime(date)}```", inline=False)
            embed.add_field(name="```Nombre de Membres```", value=f"```{str(member_count)}```", inline=True)
            embed.add_field(name="```Nombre de Channels```", value=f"```{str(channel_count)}```", inline=True)
            embed.add_field(name="```Nombre de Role```", value=f"```{str(role_count)}```", inline=True)
            embed.add_field(name="```Nombre de Boosts```", value=f"```{str(boost_count)}```", inline=True)
            embed.add_field(name="```Niveau des Boosts```", value=f"```{str(boost_tier)}```", inline=True)

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ServerinfoCommand(bot))
