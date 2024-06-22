import json

import aiohttp
import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import mods_lang as langText



class AddEmojiCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /addemoji has been loaded')

    @commands.slash_command(name='addemoji', description=langText.get("ADDEMOJI_DESCRIPTION"))
    @commands.has_permissions(manage_emojis=True)
    async def addemoji(self, ctx, emoji: disnake.PartialEmoji, name=None):
        try:
            if name is None:
                name = emoji.name

            guild = ctx.guild
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(emoji.url)) as resp:
                        if resp.status == 200:
                            image_data = await resp.read()
                            new_emoji = await guild.create_custom_emoji(name=name, image=image_data)
                            embed = disnake.Embed(
                                title=langText.get("ADDEMOJI_TITLE"),
                                description=langText.get("ADDEMOJI_TEXT").format(emoji=new_emoji),
                                color=disnake.Color.green()
                            )
                            await ctx.response.defer()
                            await ctx.send(embed=embed)
            except disnake.HTTPException:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_ADDEMOJI_TEXT"),
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AddEmojiCommand(bot))
