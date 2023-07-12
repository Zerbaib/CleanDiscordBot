import random
import disnake
from disnake.ext import commands

class DiceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /dice has been loaded')

    @commands.slash_command(name="dice", description="Play the dice game")
    async def dice(self, ctx, bet: int):
        dice_emojis = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:']
        
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)

        payout = 0

        if dice1 == dice2:  # Pair
            payout = bet * dice1

        embed = disnake.Embed(title="Dice Game", color=disnake.Color.blue())
        embed.add_field(name="Dice Roll Result", value=f"{dice_emojis[dice1 - 1]}  {dice_emojis[dice2 - 1]}", inline=False)

        if payout > 0:
            embed.add_field(name="Result", value=f"You won `{payout}` coin!")
            embed.color = disnake.Color.green()
        else:
            embed.add_field(name="Bet", value=f"`{bet}`")
            embed.add_field(name="Result", value="You lost your bet.")
            embed.color = disnake.Color.red()

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(DiceCommand(bot))
