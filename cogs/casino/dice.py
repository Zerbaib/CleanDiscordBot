import random

import disnake
from disnake.ext import commands

from utils import error
from utils.sql_manager import insertCasinoData, updateCasinoData, readData
from utils.load_lang import casino_lang as langText


class DiceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('⚠️ 🔩 /dice has been loaded')

    @commands.slash_command(name="dice", description=langText.get("DICE_DESCRIPTION"))
    async def dice(self, inter: disnake.ApplicationCommandInteraction, bet: int):
        try:
            userID = int(inter.author.id)
            dice_emojis = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:']
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            payout = 0

            if readData("casinoAccount", userID) == []:
                insertCasinoData((userID, 0))

            casinoAccount = readData("casinoAccount", userID)[0]
            userBalance = casinoAccount[2]

            if bet < 0:
                embed = disnake.Embed()
                embed.title = langText.get("ERROR_TITLE")
                embed.color = disnake.Color.red()
                embed.add_field(name="Error", value=langText.get("ERROR_NEGATIVE_BET"))
                await inter.response.send_message(embed=embed)
                return
            if bet > userBalance:
                embed = disnake.Embed()
                embed.title = langText.get("ERROR_TITLE")
                embed.color = disnake.Color.red()
                embed.add_field(name="Error", value=langText.get("ERROR_NO_MONEY"))
                await inter.response.send_message(embed=embed)
                return

            if dice1 == dice2:
                payout = bet * dice1
                userBalance += payout

                embed = disnake.Embed()
                embed.title = langText.get("DICE_TITLE")
                embed.color = disnake.Color.blue()
                embed.add_field(name=langText.get("DICE_ROLL"), value=f"{dice_emojis[dice1 - 1]}  {dice_emojis[dice2 - 1]}", inline=False)
                embed.add_field(name=langText.get("OUTCOME_TITLE"), value=langText.get("WIN_DESCRIPTION").format(win_bet=payout))
                embed.color = disnake.Color.green()
            else:
                userBalance -= bet
                embed = disnake.Embed()
                embed.title = langText.get("DICE_TITLE")
                embed.add_field(name=langText.get("DICE_ROLL"), value=f"{dice_emojis[dice1 - 1]}  {dice_emojis[dice2 - 1]}", inline=False)
                embed.add_field(name=langText.get("BET"), value=f"`{bet}`")
                embed.add_field(name=langText.get("OUTCOME_TITLE"), value=langText.get("LOST_OUTCOME"))
                embed.color = disnake.Color.red()

            updateCasinoData((userID, userBalance))
            await inter.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(DiceCommand(bot))
