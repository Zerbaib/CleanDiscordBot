import datetime
import json
import random
import time

import disnake
from disnake.ext import commands

from lang.fr.utils import error

cooldown_time = 60 * 60 * 2

class SlotCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"
        self.cooldown_file = "data/cooldown.json"
        self.min_balance = 50
        self.bet_options = {
            "rouge": "🔴",
            "noir": "⚫️",
            "pair": "🔵",
            "impair": "🟡"
        }
        self.payouts = {
            "rouge": 2,
            "noir": 2,
            "pair": 2,
            "impair": 2
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /slot has been loaded')

    @commands.slash_command(name='slot', description='Jouez à la machine à sous')
    async def slot(self, ctx, bet: int):
        try:
            if bet <= 0:
                embed = disnake.Embed(
                    title="Machine à sous",
                    description="La mise doit être supérieure à 0.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return

            with open('data/casino.json', 'r') as file:
                data = json.load(file)

            user_id = str(ctx.author.id)
            if user_id not in data:
                embed = disnake.Embed(
                    title="Machine à sous",
                    description="Vous n'avez pas de compte de casino. Utilisez ``/earn`` pour gagner des pièces.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return

            balance = data[user_id]
            if balance < bet:
                embed = disnake.Embed(
                    title="Machine à sous",
                    description="Solde insuffisant.\nVous n'avez pas assez de pièces pour placer ce pari.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return

            reels = ["🍒", "🍊", "🍋", "🍇", "🔔", "💎", "🍀", "🍎"]
            random.shuffle(reels)
            
            result = []
            for _ in range(3):
                symbol = random.choice(reels)
                result.append(symbol)
            random.shuffle(reels)
            ligne1 = []
            for _ in range(3):
                symbol = random.choice(reels)
                ligne1.append(symbol)
            ligne2 = []
            for _ in range(3):
                symbol = random.choice(reels)
                ligne2.append(symbol)
            embed = disnake.Embed(title="🎰 Machine à sous 🎰", color=disnake.Color.blurple())
            embed.add_field(name="Reels",
                            value=f"| ``{ligne1[0]} | {ligne1[1]} | {ligne1[2]}`` |\n\n"
                                f"**>** **``{result[0]} | {result[1]} | {result[2]}``** **<**\n\n"
                                f"| ``{ligne2[0]} | {ligne2[1]} | {ligne2[2]}`` |",
                            inline=False
                            )

            if result[0] == result[1] == result[2]:
                win_amount = bet * 10 
                balance += win_amount
                embed.add_field(name="Résultat",
                                value=f"Bien joué! Vous avez obtenu 3 symboles identiques et gagné **``{win_amount}``** pièces !",
                                inline=False
                                )
            else:
                balance -= bet
                embed.add_field(name="Résultat",
                                value="Désolé, vous n'avez pas gagné cette fois.",
                                inline=False
                                )

            data[user_id] = balance

            with open('data/casino.json', 'w') as file:
                json.dump(data, file, indent=4)

            embed.add_field(name="Solde",
                            value=f"Il vous reste **``{balance}``** pièces.",
                            inline=False
                            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(SlotCommand(bot))
