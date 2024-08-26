import json
import random

import disnake
from disnake.ext import commands
from utils import error
from utils.color import hex_to_discord_color
from utils.load_lang import casino_lang as langText
from utils.sql_manager import insertCasinoData, readData, updateCasinoData



discord_blue = "#7289da"
discord_red = "#ed5555"

class BetCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /bet has been loaded')

    @commands.slash_command(name="bet", description=langText.get("BET_DESCRIPTION"))
    async def bet(self, ctx, amount: int):
        try:
            userID = str(ctx.author.id)
            winChance = 25
            outcome = random.choices([True, False], weights=[winChance, 100 - winChance], k=1)[0]

            if readData("casinoAccount", userID) == []:
                insertCasinoData((userID, 0))

            casinoData = readData("casinoAccount", userID)[0]
            userBalance = casinoData[2]

            if amount < 0:
                embed = disnake.Embed(
                    title=langText.get('ERROR_TITLE'),
                    color=hex_to_discord_color(discord_red)
                    )
                embed.add_field(name=langText.get('ERROR_TITLE'), value=langText.get('ERROR_NEGATIVE_BET'))
                await ctx.response.send_message(embed=embed)
                return

            if amount > userBalance:
                embed = disnake.Embed(
                    title=langText.get('ERROR_TITLE'),
                    color=hex_to_discord_color(discord_red)
                )
                embed.add_field(name=langText.get('ERROR_TITLE'), value=langText.get('ERROR_NO_MONEY'))
                await ctx.response.send_message(embed=embed)
                return

            if outcome:
                winnings = amount * 2
                userBalance += winnings

                embed = disnake.Embed(
                    title=langText.get("WIN_TITLE"),
                    color=hex_to_discord_color(discord_blue))
                embed.add_field(
                    name=langText.get('OUTCOME_TITLE'),
                    value=langText.get('WIN_OUTCOME'),
                    inline=False)
                embed.add_field(
                    name=langText.get('WINNINGS'),
                    value=langText.get('WIN_DESCRIPTION').format(win_bet=winnings),
                    inline=False)
            else:
                userBalance -= amount

                embed = disnake.Embed(
                    title=langText.get('LOST_TITLE'),
                    color=disnake.Color.red())
                embed.add_field(
                    name=langText.get('OUTCOME_TITLE'),
                    value=langText.get('LOST_OUTCOME'))

            updateCasinoData((userID, userBalance))
            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BetCommand(bot))