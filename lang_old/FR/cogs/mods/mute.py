import json

import aiohttp
import disnake
from disnake.ext import commands

from lang.fr.utils import error


class MuteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /mute has been loaded')
        
    @commands.slash_command(name="mute", description="Mute un membre")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: disnake.Member, reason: str = "Aucune raison spécifiée"):
        try:
            with open("config.json", 'r') as config_file:
                config = json.load(config_file)
            role_id = config.get("MUTE_ROLE_ID")

            role = disnake.utils.get(ctx.guild.roles, id=role_id)
            await member.add_roles(role)

            embed = disnake.Embed(
                title="😶 Membre Muté 😶",
                description=f"{member.mention} a été muté.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Raison", value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(MuteCommand(bot))