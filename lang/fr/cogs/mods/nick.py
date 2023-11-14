import json

import aiohttp
import disnake
from disnake.ext import commands

from lang.fr.utils import error


class NickCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /nick has been loaded')
        
    @commands.slash_command(name="nick", description="Change le surnom d'un membre")
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
                        title="🥸 Surnom Changé 🥸",
                        description=f"Le surnom de {member.mention} a été changé en ``{nickname}``.",
                        color=disnake.Color.green()
                    )
                else:
                    embed = disnake.Embed(
                        title="Aucun Surnom Spécifié",
                        description=f"Aucun surnom spécifié. Le surnom reste inchangé.",
                        color=disnake.Color.orange()
                    )
                await ctx.response.defer()
                await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Permission Refusée",
                    description="Vous n'avez pas la permission de changer les surnoms des autres membres.",
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(NickCommand(bot))