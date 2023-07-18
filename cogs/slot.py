import disnake
from disnake.ext import commands
import random
import json

class SlotMachine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='slot', description='Play the slot machine')
    async def slot(self, ctx, bet: int):
        if bet <= 0:
            embed = disnake.Embed(
                title="Slot Machine",
                description="The bet must be greater than zero.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        with open('data/casino.json', 'r') as file:
            data = json.load(file)

        user_id = str(ctx.author.id)
        if user_id not in data:
            embed = disnake.Embed(
                title="Slot Machine",
                description="You are not registered in the casino. Use the `/earn` command to sign up.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        balance = data[user_id]
        if balance < bet:
            embed = disnake.Embed(
                title="Slot Machine",
                description="Insufficient balance to place the bet.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        reels = ["🍒", "🍊", "🍋", "🍇", "🔔", "💎", "🍀", "🍎"]  # Reel symbols
        random.shuffle(reels)  # Shuffle the symbols

        result = []
        for _ in range(3):
            symbol = random.choice(reels)  # Select a random symbol for each reel
            result.append(symbol)
        random.shuffle(reels)
        ligne1 = []
        for _ in range(3):
            symbol = random.choice(reels)  # Select a random symbol for each reel
            ligne1.append(symbol)
        ligne2 = []
        for _ in range(3):
            symbol = random.choice(reels)  # Select a random symbol for each reel
            ligne2.append(symbol)
        embed = disnake.Embed(title="Slot Machine", color=disnake.Color.blurple())
        embed.add_field(name="Reels",
                        value=f"| ``{ligne1[0]} | {ligne1[1]} | {ligne1[2]}`` |\n"
                              f"**> ``{result[0]} | {result[1]} | {result[2]}`` <**\n"
                              f"| ``{ligne2[0]} | {ligne2[1]} | {ligne2[2]}`` |",
                        inline=False
                        )

        if result[0] == result[1] == result[2]:
            win_amount = bet * 10  # Win 10 times the bet amount for matching all 3 reels
            balance += win_amount
            embed.add_field(name="Result", value=f"Congratulations! You won ``{win_amount}`` coins.", inline=False)
        else:
            balance -= bet
            embed.add_field(name="Result", value="Sorry! You didn't get a match.", inline=False)

        data[user_id] = balance

        with open('data/casino.json', 'w') as file:
            json.dump(data, file, indent=4)

        embed.add_field(name="Balance", value=f"Remaining balance: ``{balance}`` coins.", inline=False)
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(SlotMachine(bot))
