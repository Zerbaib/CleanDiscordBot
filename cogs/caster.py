import disnake
from disnake.ext import commands
import random
import asyncio
import json

class CasterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"
        self.bet_options = {
            "red": "🔴",
            "black": "⚫️",
            "even": "🔵",
            "odd": "🟡"
        }
        self.payouts = {
            "red": 2,
            "black": 2,
            "even": 2,
            "odd": 2
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /caster has been loaded')

    @commands.slash_command(name="caster", description="Play a game of caster")
    async def caster(self, ctx, bet_option: str, bet_amount: int):
        user_id = str(ctx.author.id)
        bet_option = bet_option.lower()

        if bet_option not in self.bet_options:
            embed = disnake.Embed(
                title="Caster",
                description="Invalid bet option.\n\nPlease choose from ``red``, ``black``, ``even``, ``odd``.",
                color=disnake.Color.red()
            )
            await ctx.response.send_message(embed=embed)
            return

        if bet_amount <= 0:
            embed = disnake.Embed(
                title="Caster",
                description="Invalid bet amount.\nPlease enter a positive value.",
                color=disnake.Color.red()
            )
            await ctx.response.send_message(embed=embed)
            return

        with open(self.data_file, 'r') as file:
            data = json.load(file)

        balance = data.get(user_id, 0)

        if balance < bet_amount:
            embed = disnake.Embed(
                title="Caster",
                description="Insufficient balance.\nYou don't have enough coins to place this bet.",
                color=disnake.Color.red()
            )
            await ctx.response.send_message(embed=embed)
            return

        result = random.choice(list(self.bet_options.keys()))
        payout = self.payouts.get(bet_option, 0)

        embed = disnake.Embed(
            title="Caster",
            description=f"The caster rolls...",
            color=disnake.Color.blue()
        )
        try:
            message = await ctx.message.send(embed=embed)
        except disnake.errors.InteractionResponded:
            return

        if result == bet_option:
            winnings = bet_amount * payout
            balance += winnings
            embed = disnake.Embed(
                title="Caster",
                description=f"Congratulations! You won {self.bet_options[result]}\nand **`{winnings}`** coins!",
                color=disnake.Color.green()
            )
        else:
            balance -= bet_amount
            embed = disnake.Embed(
                title="Caster",
                description=f"Sorry, you lost your bet.\nThe caster rolled {self.bet_options[result]}.",
                color=disnake.Color.red()
            )

        await asyncio.sleep(2)
        await message.edit(embed=embed)

        data[user_id] = balance

        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

def setup(bot):
    bot.add_cog(CasterCommand(bot))
