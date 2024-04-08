import json

import aiohttp
import disnake
from disnake.ext import commands

from cogs.utils import error
from cogs.utils.color import hex_to_discord_color
from cogs.utils.embed import create_embed
from cogs.utils.lang_loader import load_mods_lang

langText = load_mods_lang()


class BanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /ban has been loaded')
        
    @commands.slash_command(name="ban", description=langText.get("BAN_DESCRIPTION"))
    async def ban(self, ctx, user: disnake.User, reason: str = langText.get("NOREASON")):
        try:
            member = ctx.guild.get_member(ctx.author.id)
            bot = ctx.guild.get_member(self.bot.user.id)
            if member.guild_permissions.ban_members:
                if bot.guild_permissions.ban_members:
                    await ctx.guild.ban(user, reason=reason)
                    embed = disnake.Embed(
                        title=langText.get("BAN_TITLE"),
                        description=langText.get("BAN_TEXT").format(user=user.name, userDisplay=user.display_name),
                        color=disnake.Color.dark_red()
                        )
                    embed.add_field(name=langText.get("BAN_REASON"), value=f"`{reason}`")
                    await ctx.response.defer()
                    await ctx.send(embed=embed)
                else:
                    embed = disnake.Embed(
                        title=langText.get("ERROR_TITLE"),
                        description=langText.get("ERROR_BAN_BOTNOPERMISSION"),
                        color=disnake.Color.red()
                    )
                    await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_BAN_USERNOPERMISSION"),
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(BanCommand(bot))