import json
import random

import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import casino_lang as langText



class SlotCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /slot has been loaded')

    @commands.slash_command(name='slot', description=langText.get("SLOTS_DESCRIPTION"))
    async def slot(self, ctx, bet: int):
        try:
            if bet <= 0:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_NEGATIVE_BET"),
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return

            with open('data/casino.json', 'r') as file:
                data = json.load(file)

            user_id = str(ctx.author.id)
            if user_id not in data:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_NOT_REGISTERED"),
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return

            balance = data[user_id]
            if balance < bet:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_NO_MONEY"),
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
            embed = disnake.Embed(title=langText.get("SLOTS_TITLE"), color=disnake.Color.blurple())
            embed.add_field(name="Reels",
                            value=f"| ``{ligne1[0]} | {ligne1[1]} | {ligne1[2]}`` |\n\n"
                                f"**>** **``{result[0]} | {result[1]} | {result[2]}``** **<**\n\n"
                                f"| ``{ligne2[0]} | {ligne2[1]} | {ligne2[2]}`` |",
                            inline=False
                            )

            if result[0] == result[1] == result[2]:
                win_amount = bet * 10  # Win 10 times the bet amount for matching all 3 reels
                balance += win_amount
                
                winDescription = langText.get("WIN_DESCRIPTION")
                formatted_win_description = winDescription.format(win_bet=win_amount)
                
                embed.add_field(name=langText.get("WIN_OUTCOME"), value=formatted_win_description, inline=False)
            else:
                balance -= bet
                embed.add_field(name=langText.get("OUTCOME_TITLE"), value=langText.get("LOST_OUTCOME"), inline=False)

            data[user_id] = balance

            with open('data/casino.json', 'w') as file:
                json.dump(data, file, indent=4)

            balanceDescription = langText.get("REMAINING_BALANCE")
            formatted_balance_description = balanceDescription.format(bal=balance)

            embed.add_field(name="Balance", value=formatted_balance_description, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(SlotCommand(bot))
