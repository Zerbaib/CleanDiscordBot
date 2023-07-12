import disnake
from disnake.ext import commands
import json
import random

class BetCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"
        self.min_balance = 50

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /bet has been loaded')

    @commands.slash_command(name="bet", description="Bet coins | x2 or lost")
    async def bet(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        with open(self.data_file, 'r+') as file:
            data = json.load(file)
            balance = data.get(user_id, 0)
            if amount <= 0 or amount > balance:
                embed = disnake.Embed(title="Invalid Bet Amount", color=disnake.Color.red())
                embed.add_field(name="Error", value="Invalid bet amount!")
                await ctx.response.send_message(embed=embed)
                return
            if balance < self.min_balance:
                embed = disnake.Embed(title="Insufficient Balance", color=disnake.Color.red())
                embed.add_field(name="Error", value=f"You need at least {self.min_balance} coins to play!")
                await ctx.response.send_message(embed=embed)
                return

            # Game logic: Quitte ou Double
            win_chance = 25  # 25% chance of winning, 75% chance of losing
            outcome = random.choices([True, False], weights=[win_chance, 100 - win_chance], k=1)[0]

            if outcome:
                winnings = amount * 2
                data[user_id] += winnings
                embed = disnake.Embed(title="💰 You Won!", color=disnake.Color.green())
                embed.add_field(name="Outcome", value="Congratulations! You won the bet.", inline=False)
                embed.add_field(name="Winnings", value=f"You won `{winnings}` coins!", inline=False)
                await ctx.response.send_message(embed=embed)
            else:
                data[user_id] -= amount
                embed = disnake.Embed(title="😢 You Lost", color=disnake.Color.red())
                embed.add_field(name="Outcome", value="Better luck next time. You lost the bet.")
                await ctx.response.send_message(embed=embed)

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

def setup(bot):
    bot.add_cog(BetCommand(bot))
