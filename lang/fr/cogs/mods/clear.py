import json

import aiohttp
import disnake
from disnake.ext import commands

from lang.fr.utils import error


class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /clear has been loaded')
        
    @commands.slash_command(name="clear", description="Efface un nombre spécifié de messages dans le salon")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount)

            embed = disnake.Embed(
                title="🌪 Messages Effacés 🌪",
                description=f"``{amount}`` messages ont été effacés dans ce salon.",
                color=disnake.Color.brand_green()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed, delete_after=3)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(ClearCommand(bot))