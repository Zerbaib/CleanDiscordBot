import json

import aiohttp
import disnake
from disnake.ext import commands
from utils import error
from utils.load_lang import mods_lang as langText
from modules.var import *



class MuteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /mute has been loaded')
        
    @commands.slash_command(name="mute", description=langText.get("MUTE_DESCRIPTION"))
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: disnake.Member, reason: str = langText.get("NOREASON")):
        try:
            with open(files.config, 'r') as config_file:
                config = json.load(config_file)
            role_id = config.get("MUTE_ROLE_ID")

            role = disnake.utils.get(ctx.guild.roles, id=role_id)
            await member.add_roles(role)

            embed = disnake.Embed(
                title=langText.get("MUTE_TITLE"),
                description=langText.get("MUTE_TEXT").format(user=member.name, userDisplay=member.display_name),
                color=disnake.Color.dark_red()
            ) 
            embed.add_field(name=langText.get("REASON"), value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(MuteCommand(bot))