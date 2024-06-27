import json
import random

import disnake
from disnake.ext import commands

from utils import error
from utils.sql_manager import insertCasinoData, updateCasinoData, readData
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
            userID = str(ctx.author.id)
            reels = ["🍒", "🍊", "🍋", "🍇", "🔔", "💎", "🍀", "🍎"]
            random.shuffle(reels)
            result = []
            ligne1 = []
            ligne2 = []

            if readData("casinoAccount", userID) == []:
                insertCasinoData((userID, 0))

            casinoAccount = readData("casinoAccount", userID)[0]
            userBalance = casinoAccount[2]

            if bet < 0:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_NEGATIVE_BET"),
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return
            if bet > userBalance:
                embed = disnake.Embed()
                embed.title = langText.get("ERROR_TITLE")
                embed.color = disnake.Color.red()
                embed.add_field(name="Error", value=langText.get("ERROR_NO_MONEY"))
                await inter.response.send_message(embed=embed)
                return

            for _ in range(3):
                symbol = random.choice(reels)
                result.append(symbol)
            for _ in range(3):
                symbol = random.choice(reels)  # Select a random symbol for each reel
                ligne1.append(symbol)
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
                win_amount = bet * 10
                userBalance += win_amount
                embed.add_field(name=langText.get("WIN_OUTCOME"), value=langText.get("WIN_DESCRIPTION").format(win_bet=win_amount), inline=False)
            else:
                userBalance -= bet
                embed.add_field(name=langText.get("OUTCOME_TITLE"), value=langText.get("LOST_OUTCOME"), inline=False)

            embed.add_field(name="Balance", value=langText.get("REMAINING_BALANCE").format(bal=userBalance), inline=False)

            updateCasinoData((userID, userBalance))

            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(SlotCommand(bot))
