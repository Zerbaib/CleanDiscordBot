import asyncio
import random

import disnake
from disnake.ext import commands

from lang.fr.utils import error


class GuessCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /findnumber has been loaded')
        print('🔩 /guess has been loaded')

    @commands.slash_command(name='findnumber', description="Essayer de trouver le nombre !")
    async def findnumber(self, ctx):
        try:
            if ctx.author.id in self.games:
                embed = disnake.Embed(
                    title="Erreur",
                    description="Tu joues déjà au jeu. Utilise **``/guess``** pour continuer.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
            else:
                number = random.randint(1, 10000)
                self.games[ctx.author.id] = {
                    "number": number,
                    "attempts": 0
                }

                embed = disnake.Embed(
                    title="Trouver le nombre! 🔢",
                    description="J'ai choisi un nombre entre `1` et `10000`. Devine le nombre!",
                    color=disnake.Color.blurple()
                )
                embed.set_footer(text="Utilise `/guess <nombre>` pour deviner le nombre.")
                embed.add_field(name="Instructions:",
                                value="Trouvez le nombre que j'ai choisi. Vous avez 25 tentatives.",
                                inline=False)
                embed.add_field(name="Tentatives", value="``0/25``", inline=False)

                await ctx.response.defer()
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name='guess', description="Trouver le nombre !")
    async def guess(self, ctx, number: int):
        try:
            if ctx.author.id not in self.games:
                embed = disnake.Embed(
                    title="Erreur",
                    description="Tu n'a pas commencé le jeu. Utilise **``/findnumber``** pour commencer.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
            else:
                game = self.games[ctx.author.id]
                correct_number = game["number"]
                attempts = game["attempts"] + 1
                self.games[ctx.author.id]["attempts"] = attempts

                if number == correct_number:
                    embed = disnake.Embed(
                        title="Bravo ! 🎉",
                        description="Tu as trouvé le bon nombre !",
                        color=disnake.Color.green()
                    )
                    embed.add_field(name="Ton nombre:", value=f"`{number}`", inline=False)
                    embed.add_field(name="Mon nombre:", value=f"``{correct_number}``", inline=False)
                    del self.games[ctx.author.id]
                elif attempts >= 25:
                    embed = disnake.Embed(
                        title="Perdu ! 😢",
                        description="Tu as dépassé le nombre de tentatives. Tu as perdu.",
                        color=disnake.Color.red()
                    )
                    embed.add_field(name="Ton nombre:", value=f"``{number}``", inline=False)
                    embed.add_field(name="Mon nombre:", value=f"`{correct_number}`", inline=False)
                    del self.games[ctx.author.id]
                elif number < correct_number:
                    embed = disnake.Embed(
                        title="Trop bas! ⬆️",
                        description="Essaye un nombre plus grand.",
                        color=disnake.Color.old_blurple()
                    )
                    embed.add_field(name="Ton nombre:", value=f"``{number}``", inline=False)
                    embed.add_field(name="Mon nombre:", value=f"``{attempts}/25``", inline=False)
                else:
                    embed = disnake.Embed(
                        title="Très haut! ⬇️",
                        description="Essaye un nombre plus petit.",
                        color=disnake.Color.old_blurple()
                    )
                    embed.add_field(name="Ton nombre:", value=f"``{number}``", inline=False)
                    embed.add_field(name="Mon nombre:", value=f"``{attempts}/25``", inline=False)

                await ctx.response.defer()
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GuessCommands(bot))