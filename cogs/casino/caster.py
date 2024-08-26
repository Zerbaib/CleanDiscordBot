import random

import disnake
from disnake.ext import commands
from utils import error
from utils.load_lang import casino_lang as langText
from utils.sql_manager import insertCasinoData, readData, updateCasinoData



class CasterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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

    @commands.slash_command(name="caster", description=langText.get("CASTER_DESCRIPTION"))
    async def caster(self, ctx, bet_option: str, bet_amount: int):
        try:
            userID = str(ctx.author.id)
            bet_option = bet_option.lower()

            if readData("casinoAccount", userID) == []:
                insertCasinoData((userID, 0))

            casinoAccount = readData("casinoAccount", userID)[0]
            userBalance = casinoAccount[2]

            if not bet_option in self.bet_options:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_INVALID_OPTION"),
                    color=disnake.Color.red())
                await ctx.send(embed=embed)
                return
            if bet_amount < 0:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_NEGATIVE_BET"),
                    color=disnake.Color.red())
                await ctx.send(embed=embed)
                return
            if bet_amount > userBalance:
                embed = disnake.Embed(
                    title=langText.get('ERROR_TITLE'),
                    color=disnake.Color.red())
                embed.add_field(name=langText.get('ERROR_TITLE'), value=langText.get('ERROR_NO_MONEY'))
                await ctx.send(embed=embed)
                return

            result = random.choice(list(self.bet_options.keys()))
            resultEmoji = self.bet_options[result]
            payout = self.payouts.get(bet_option, 0)

            if result == bet_option:
                winnings = bet_amount * payout
                userBalance += winnings

                embed = disnake.Embed(
                    title=langText.get("CASTER_TITLE"),
                    description=langText.get("CASTER_WIN_DESCRIPTION").format(result=resultEmoji, winnings=winnings),
                    color=disnake.Color.green())
            else:
                userBalance -= bet_amount
                embed = disnake.Embed(
                    title=langText.get("CASTER_TITLE"),
                    description=langText.get("CASTER_LOSE_DESCRIPTION").format(result=resultEmoji),
                    color=disnake.Color.red())

            updateCasinoData((userID, userBalance))
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CasterCommand(bot))