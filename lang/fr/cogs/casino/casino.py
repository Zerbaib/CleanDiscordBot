import datetime
import json
import random
import time

import disnake
from disnake.ext import commands

from lang.fr.utils import error

cooldown_time = 60 * 60 * 2

class CasinoCommands(commands.Cog):
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
        print('========== ⚙️ Casino ⚙️ ==========')
        print('🔩 /dice has been loaded')
        print('🔩 /caster has been loaded')
        print('🔩 /slot has been loaded')
        print()


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
    bot.add_cog(CasinoCommands(bot))
