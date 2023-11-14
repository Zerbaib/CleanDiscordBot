import json

import aiohttp
import disnake
from disnake.ext import commands

from lang.fr.utils import error


class AddemojiCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /addemoji has been loaded')

    @commands.slash_command(name='addemoji', description="Ajoute un emoji au serveur.")
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
                                title='✨ Emoji ajouté ✨',
                                description=f"L'emoji {new_emoji} a été ajouté avec succès :tada:",
                                color=disnake.Color.green()
                            )
                            await ctx.response.defer()
                            await ctx.send(embed=embed)
            except disnake.HTTPException:
                embed = disnake.Embed(
                    title='Erreur',
                    description="Une erreur s'est produite lors de l'ajout de l'emoji :x:",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AddemojiCommand(bot))