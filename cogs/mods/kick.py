import json

import aiohttp
import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import mods_lang as langText



class KickCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /kick has been loaded')
        
    @commands.slash_command(name="kick", description=langText.get("KICK_DESCRIPTION"))
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: disnake.Member, reason: str = langText.get("NOREASON")):
        try:
            await user.kick(reason=reason)

            embed = disnake.Embed(
                title=langText.get("KICK_TITLE"),
                description=langText.get("KICK_TEXT").format(user=user.name, userDisplay=user.display_name),
                color=disnake.Color.dark_red()
            )
            embed.add_field(name=langText.get("REASON"), value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(KickCommand(bot))