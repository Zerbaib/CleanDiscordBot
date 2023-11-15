import json
import random

import disnake
from disnake.ext import commands

from lang.en.utils import error

class BetCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /bet has been loaded')

    @commands.slash_command(name="bet", description="Bet coins | x2 or lost")
    async def bet(self, ctx, amount: int):
        try:
            user_id = str(ctx.author.id)
            win_chance = 25
            outcome = random.choices([True, False], weights=[win_chance, 100 - win_chance], k=1)[0]
            with open(self.data_file, 'r+') as file:
                data = json.load(file)
                balance = data.get(user_id, 0)
                if amount > 0:
                    if amount <= balance:
                        if outcome:
                            winnings = amount * 2
                            data[user_id] += winnings
                            embed = disnake.Embed(title="💰 You Won!", color=disnake.Color.green())
                            embed.add_field(name="Outcome", value="Congratulations! You won the bet.", inline=False)
                            embed.add_field(name="Winnings", value=f"You won `{winnings}` coins!", inline=False)
                            await ctx.response.defer()
                            await ctx.send(embed=embed)
                        else:
                            data[user_id] -= amount
                            embed = disnake.Embed(title="😢 You Lost", color=disnake.Color.red())
                            embed.add_field(name="Outcome", value="Better luck next time. You lost the bet.")
                            await ctx.response.defer()
                            await ctx.send(embed=embed)
                    else:
                        embed = disnake.Embed(title="You cant play", color=disnake.Color.red())
                        embed.add_field(name="Error", value="You don't have enough money")
                        await ctx.response.send_message(embed=embed)
                else:
                    embed = disnake.Embed(title="You cant play", color=disnake.Color.red())
                    embed.add_field(name="Error", value="You can't play with a negative number")
                    await ctx.response.send_message(embed=embed)
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BetCommand(bot))