import json

import aiohttp
import disnake
from disnake.ext import commands

from lang.fr.utils import error


class UnmuteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /unmute has been loaded')
        
    @commands.slash_command(name="unmute", description="Unmute un membre")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: disnake.Member, reason: str = "Aucune raison spécifiée"):
        try:
            with open("config.json", 'r') as config_file:
                config = json.load(config_file)
            role_id = config.get("MUTE_ROLE_ID")

            role = disnake.utils.get(ctx.guild.roles, id=role_id)
            if role and role in member.roles:
                await member.remove_roles(role)

            embed = disnake.Embed(
                title="😐 Membre Démué 😐",
                description=f"{member.mention} a été démuet.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Raison", value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
           
def setup(bot):
    bot.add_cog(UnmuteCommand(bot))