import datetime
import json
import random
import time

import disnake
from disnake.ext import commands

from lang.fr.utils import error

cooldown_time = 60 * 60 * 2

class CasterCommand(commands.Cog):
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
        print('🔩 /caster has been loaded')
        
    @commands.slash_command(name="caster", description="Jouez à la roulette")
    async def caster(self, ctx, bet_option: str, bet_amount: int):
        try:
            user_id = str(ctx.author.id)
            bet_option = bet_option.lower()

            if bet_option in self.bet_options:
                if bet_amount < 0:
                    with open(self.data_file, 'r') as file:
                        data = json.load(file)
                    balance = data.get(user_id, 0)
                    if balance > bet_amount:
                        result = random.choice(list(self.bet_options.keys()))
                        payout = self.payouts.get(bet_option, 0)
                        if result == bet_option:
                            winnings = bet_amount * payout
                            balance += winnings
                            embed = disnake.Embed(
                                title="Roulette",
                                description=f"Toutes nos félicitations! Vous avez gagné {self.bet_options[result]}\net **`{winnings}`** pièces !",
                                color=disnake.Color.green()
                            )
                        else:
                            balance -= bet_amount
                            embed = disnake.Embed(
                                title="Roulette",
                                description=f"Désolé, vous avez perdu votre pari.\nLe lanceur a lancé {self.bet_options[result]}.",
                                color=disnake.Color.red()
                            )
                        
                        await ctx.response.defer()
                        await ctx.send(embed=embed)

                        data[user_id] = balance

                        with open(self.data_file, 'w') as file:
                            json.dump(data, file, indent=4)
                    else:
                        embed = disnake.Embed(
                            title="Roulette",
                            description="Solde insuffisant.\nVous n'avez pas assez de pièces pour placer ce pari.",
                            color=disnake.Color.red()
                        )
                        await ctx.response.send_message(embed=embed)
                        return
                else:
                    embed = disnake.Embed(
                        title="Roulette",
                        description="Montant de pari invalide.\nVeuillez saisir une valeur positive.",
                        color=disnake.Color.red()
                    )
                    await ctx.response.send_message(embed=embed)
                    return
            else:
                embed = disnake.Embed(
                    title="Roulette",
                    description="Option de pari invalide.\n\nVeuillez choisir entre ``rouge``, ``noir``, ``pair`` et ``impair``.",
                    color=disnake.Color.red()
                )
                await ctx.response.send_message(embed=embed)
                return
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(CasterCommand(bot))