import json

import aiohttp
import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import mods_lang as langText


class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /clear has been loaded')

    @commands.slash_command(name="clear", description=langText.get("CLEAR_DESCRIPTION"))
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        try:
            await ctx.response.defer()
            await ctx.channel.purge(limit=amount+1)

            embed = disnake.Embed(
                title=langText.get("CLEAR_TITLE"),
                description=langText.get("CLEAR_TEXT").format(amount=amount),
                color=disnake.Color.brand_green())
            message = await ctx.send(embed=embed, delete_after=3)
            await ctx.response.send_message(message)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ClearCommand(bot))