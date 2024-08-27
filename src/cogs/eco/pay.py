import json

import disnake
from disnake.ext import commands
from utils import error
from utils.load_lang import economy_lang as langText
from utils.sql_manager import insertCasinoData, readData, updateCasinoData



class PayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /pay has been loaded')

    @commands.slash_command(name="pay", description=langText.get("PAY_DESCRIPTION"))
    async def pay(self, ctx, amount: int, user: disnake.Member):
        try:
            if user.bot:
                embed = disnake.Embed(
                    title=langText.get("ERROR_INVALID_USER_TITLE"),
                    description=langText.get("ERROR_INVALID_USER_DESCRIPTION"),
                    color=disnake.Color.red())
                return

            localUserID = str(ctx.author.id)
            exernUserID = str(user.id)

            if readData("casinoAccount", localUserID) == []:
                insertCasinoData((localUserID, 0))
            if readData("casinoAccount", exernUserID) == []:
                insertCasinoData((exernUserID, 0))

            localCasinoAccount = readData("casinoAccount", localUserID)[0]
            localUserBalance = localCasinoAccount[2]
            exernCasinoAccount = readData("casinoAccount", exernUserID)[0]
            exernUserBalance = exernCasinoAccount[2]

            if amount < 0:
                embed = disnake.Embed(
                    title=langText.get("ERROR_INVALID_AMOUNT_TITLE"),
                    description=langText.get("ERROR_INVALID_AMOUNT_DESCRIPTION"),
                    color=disnake.Color.red())
                return
            if localUserBalance <= amount:
                embed = disnake.Embed(
                    title=langText.get("ERROR_INSUFFICIENT_FUNDS_TITLE"),
                    description=langText.get("ERROR_INSUFFICIENT_FUNDS_DESCRIPTION"),
                    color=disnake.Color.red())
                return

            localUserBalance -= amount
            exernUserBalance += amount

            embed = disnake.Embed(
                title=langText.get("PAY_TITLE"),
                description=langText.get("PAY_DESCRIPTION").format(amount=amount, user=user.mention),
                color=disnake.Color.green())

            updateCasinoData((localUserID, localUserBalance))
            updateCasinoData((exernUserID, exernUserBalance))

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(PayCommand(bot))
