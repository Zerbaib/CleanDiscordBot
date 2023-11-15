import datetime
import json
import random
import time

import disnake
from disnake.ext import commands

from lang.fr.utils import error

cooldown_time = 60 * 60 * 2

class BetCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"
        self.cooldown_file = "data/cooldown.json"
        self.min_balance = 50
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /bet has been loaded')
        
    @commands.slash_command(name="bet", description="Le jeux du quitte ou double")
    async def bet(self, ctx, amount: int):
        try:
            user_id = str(ctx.author.id)
            with open(self.data_file, 'r+') as file:
                data = json.load(file)
                balance = data.get(user_id, 0)
                if amount <= 0 or amount > balance:
                    embed = disnake.Embed(title="Montant de pari invalide", color=disnake.Color.red())
                    embed.add_field(name="Erreur", value="Montant de pari invalide")
                    await ctx.response.send_message(embed=embed)
                    return
                if balance < self.min_balance:
                    embed = disnake.Embed(title="Solde insuffisant", color=disnake.Color.red())
                    embed.add_field(name="Erreur", value=f"Vous avez besoin d'au moins {self.min_balance} pièces pour jouer !")
                    await ctx.response.send_message(embed=embed)
                    return

                win_chance = 25
                outcome = random.choices([True, False], weights=[win_chance, 100 - win_chance], k=1)[0]

                if outcome:
                    winnings = amount * 2
                    data[user_id] += winnings
                    embed = disnake.Embed(title="💰 Tu as gagné!", color=disnake.Color.green())
                    embed.add_field(name="Résultat", value="Toutes nos félicitations! Vous avez gagné le pari.", inline=False)
                    embed.add_field(name="Gains", value=f"Vous avez gagné des pièces `{winnings}` !", inline=False)
                    await ctx.response.defer()
                    await ctx.send(embed=embed)
                else:
                    data[user_id] -= amount
                    embed = disnake.Embed(title="😢 Tu as perdu", color=disnake.Color.red())
                    embed.add_field(name="Résultat", value="Better luck next time. You lost the bet.")
                    await ctx.response.defer()
                    await ctx.send(embed=embed)

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BetCommand(bot))