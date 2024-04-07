import json

import aiohttp
import disnake
from disnake.ext import commands

from lang.en.utils import error


class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /clear has been loaded')

    @commands.slash_command(name="clear", description="Clear a specified number of messages in the channel")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount)

            embed = disnake.Embed(
                title="🌪 Messages Cleared 🌪",
                description=f"``{amount}`` messages have been cleared in this channel.",
                color=disnake.Color.brand_green()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed, delete_after=3)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(ClearCommand(bot))