import json

import aiohttp
import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import load_mods_lang

langText = load_mods_lang()


class NickCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /nick has been loaded')
        
    @commands.slash_command(name="nick", description=langText.get("NICK_DESCRIPTION"))
    async def nick(self, ctx, member: disnake.Member = None, *, nickname: str = None):
        try:
            if member is None:
                member = ctx.author
            if nickname is None:
                nickname = member.name

            if member == ctx.author or ctx.author.guild_permissions.manage_nicknames:
                if nickname is not None:
                    await member.edit(nick=nickname)

                if nickname is not None:
                    embed = disnake.Embed(
                        title=langText.get("NICK_TITLE"),
                        description=langText.get("NICK_TEXT").format(user=member.name, userDisplay=member.display_name, nickname=nickname),
                        color=disnake.Color.green()
                    )
                else:
                    embed = disnake.Embed(
                        title=langText.get("ERROR_TITLE"),
                        description=langText.get("ERROR_NICK_NONICKNAME"),
                        color=disnake.Color.orange()
                    )
                await ctx.response.defer()
                await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_NICK_NOPERMISSION"),
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(NickCommand(bot))