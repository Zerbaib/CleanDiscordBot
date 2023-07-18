import disnake
from disnake.ext import commands
import random
import json

class SlotMachine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='slot', description='Joue à la machine à sous')
    async def slot(self, ctx, bet: int):
        if bet <= 0:
            embed = disnake.Embed(
                title="Machine à sous",
                description="La mise doit être supérieure à zéro.",
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
                description="Vous n'êtes pas enregistré dans le casino. Utilisez la commande `/earn` pour vous inscrire.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        balance = data[user_id]
        if balance < bet:
            embed = disnake.Embed(
                title="Machine à sous",
                description="Solde insuffisant pour effectuer la mise.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        reels = ["🍒", "🍊", "🍋", "🍇", "🔔", "💎", "🍀", "🍎"]  # Symboles des rouleaux
        random.shuffle(reels)  # Mélanger les symboles

        result = []
        for _ in range(3):
            symbol = random.choice(reels)  # Sélectionner un symbole aléatoire pour chaque rouleau
            result.append(symbol)

        embed = disnake.Embed(title="Machine à sous", color=disnake.Color.blurple())
        embed.add_field(name="Rouleaux", value=f"{result[0]} | {result[1]} | {result[2]}", inline=False)

        if result[0] == result[1] == result[2]:
            win_amount = bet * 10  # Gagner 10 fois la mise en cas de correspondance sur les 3 rouleaux
            balance += win_amount
            embed.add_field(name="Résultat", value=f"Félicitations ! Vous avez gagné {win_amount} pièces.", inline=False)
        else:
            balance -= bet
            embed.add_field(name="Résultat", value="Dommage ! Vous n'avez pas obtenu de correspondance.", inline=False)

        data[user_id] = balance

        with open('data/casino.json', 'w') as file:
            json.dump(data, file, indent=4)

        embed.add_field(name="Solde", value=f"Solde restant : {balance} pièces.", inline=False)
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(SlotMachine(bot))
