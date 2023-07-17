import random
import disnake
from disnake.ext import commands
import json

class DiceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /dice has been loaded')

    @commands.slash_command(name="dice", description="Play the dice game")
    async def dice(self, ctx, bet: int):
        user_id = str(ctx.author.id)
        with open(self.data_file, 'r') as file:
            data = json.load(file)
        
        bal = data[user_id]

        if bal < bet:
            embed = disnake.Embed(title="Dice Game", color=disnake.Color.red())
            embed.add_field(name="You cant play !", value=f"You don't have money to play ``{bet}`` coin try with less.", inline=False)
            await ctx.send(embed=embed)
        else:
            dice_emojis = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:']
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)

            payout = 0

            if dice1 == dice2:  # Pair
                payout = bet * dice1

            embed = disnake.Embed(title="Dice Game", color=disnake.Color.blue())
            embed.add_field(name="Dice Roll Result", value=f"{dice_emojis[dice1 - 1]}  {dice_emojis[dice2 - 1]}", inline=False)

            if payout > 0:
                data[user_id] += payout
                embed.add_field(name="Result", value=f"You won `{payout}` coin!")
                embed.color = disnake.Color.green()
            else:
                data[user_id] -= bet
                embed.add_field(name="Bet", value=f"`{bet}`")
                embed.add_field(name="Result", value="You lost your bet.")
                embed.color = disnake.Color.red()

            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)

            await ctx.response.defer()
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(DiceCommand(bot))
