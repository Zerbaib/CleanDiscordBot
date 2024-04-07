import json

import aiohttp
import disnake
from disnake.ext import commands

from lang.fr.utils import error


class KickCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /kick has been loaded')
        
    @commands.slash_command(name="kick", description="Expulse un utilisateur du serveur")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: disnake.Member, reason: str = "Aucune raison spécifiée"):
        try:
            await user.kick(reason=reason)

            embed = disnake.Embed(
                title="🏌️‍♀️ Utilisateur Expulsé 🏌️‍♀️",
                description=f"**{user.name}** *alias ``{user.display_name}``* a été expulsé du serveur.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Raison", value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(KickCommand(bot))