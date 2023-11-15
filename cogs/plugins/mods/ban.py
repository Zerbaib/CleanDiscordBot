import json

import aiohttp
import disnake
from disnake.ext import commands

from cogs.utils import error
from cogs.utils.color import hex_to_discord_color
from cogs.utils.embed import create_embed


class BanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /ban has been loaded')
        
    @commands.slash_command(name="ban", description="Ban a user from the server")
    async def ban(self, ctx, user: disnake.User, reason: str = "No reason provided"):
        try:
            member = ctx.guild.get_member(ctx.author.id)
            bot = ctx.guild.get_member(self.bot.user.id)
            if member.guild_permissions.ban_members:
                if bot.guild_permissions.ban_members:
                    await ctx.guild.ban(user, reason=reason)
                    embed = disnake.Embed(
                        title="🔨 User Banned 🔨",
                        description=f"**{user.name}** *aka ``{user.display_name}``* has been banned from the server.",
                        color=disnake.Color.dark_red()
                        )
                    embed.add_field(name="Reason", value=f"`{reason}`")
                    await ctx.response.defer()
                    await ctx.send(embed=embed)
                else:
                    embed = disnake.Embed(
                        title="Error",
                        description="I don't have the permission to ban users.",
                        color=disnake.Color.red()
                    )
                    await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Error",
                    description="You don't have the permission to ban users.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(BanCommand(bot))