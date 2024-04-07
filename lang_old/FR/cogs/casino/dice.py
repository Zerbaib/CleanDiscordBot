import datetime
import json
import random
import time

import disnake
from disnake.ext import commands

from lang.fr.utils import error

cooldown_time = 60 * 60 * 2

class DiceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"
        self.cooldown_file = "data/cooldown.json"
        self.min_balance = 50
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /dice has been loaded')
    
    @commands.slash_command(name="dice", description="Jouez au jeu de dés")
    async def dice(self, ctx, bet: int):
        try:
            user_id = str(ctx.author.id)
            with open(self.data_file, 'r') as file:
                data = json.load(file)
            
            bal = data[user_id]

            if bal < bet:
                embed = disnake.Embed(title="Jeu de dés", color=disnake.Color.red())
                embed.add_field(name="Tu ne peux pas jouer !", value=f"Vous n'avez pas d'argent pour jouer à ``{bet}`` esseye avec moins.", inline=False)
                await ctx.send(embed=embed)
            else:
                dice_emojis = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:']
                dice1 = random.randint(1, 6)
                dice2 = random.randint(1, 6)

                payout = 0

                if dice1 == dice2:  # Pair
                    payout = bet * dice1

                embed = disnake.Embed(title="🎲 Jeu de dés 🎲", color=disnake.Color.blue())
                embed.add_field(name="Résultat du lancer de dés", value=f"{dice_emojis[dice1 - 1]}  {dice_emojis[dice2 - 1]}", inline=False)

                if payout > 0:
                    data[user_id] += payout
                    embed.add_field(name="Résultat", value=f"Vous avez gagné la pièce `{payout}` !")
                    embed.color = disnake.Color.green()
                else:
                    data[user_id] -= bet
                    embed.add_field(name="Pari", value=f"`{bet}`")
                    embed.add_field(name="Résultat", value="Vous avez perdu votre pari.")
                    embed.color = disnake.Color.red()

                with open(self.data_file, 'w') as file:
                    json.dump(data, file, indent=4)

                await ctx.response.defer()
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(DiceCommand(bot))