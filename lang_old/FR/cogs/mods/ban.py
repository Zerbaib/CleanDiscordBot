import json

import aiohttp
import disnake
from disnake.ext import commands

from lang.fr.utils import error


class BanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /ban has been loaded')
        
    @commands.slash_command(name="ban", description="Bannir un utilisateur du serveur")
    async def ban(self, ctx, user: disnake.User, reason: str = "Aucune raison spécifiée"):
        try:
            member = ctx.guild.get_member(ctx.author.id)
            bot = ctx.guild.get_member(self.bot.user.id)
            if member.guild_permissions.ban_members:
                if bot.guild_permissions.ban_members:
                    await ctx.guild.ban(user, reason=reason)
                    embed = disnake.Embed(
                        title="🔨 Utilisateur Banni 🔨",
                        description=f"**{user.name}** *alias ``{user.display_name}``* a été banni du serveur.",
                        color=disnake.Color.dark_red()
                    )
                    embed.add_field(name="Raison", value=f"`{reason}`")
                    await ctx.response.defer()
                    await ctx.send(embed=embed)
                else:
                    embed = disnake.Embed(
                        title="Erreur",
                        description="Je n'ai pas la permission de bannir les utilisateurs.",
                        color=disnake.Color.red()
                    )
                    await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Erreur",
                    description="Vous n'avez pas la permission de bannir les utilisateurs.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BanCommand(bot))