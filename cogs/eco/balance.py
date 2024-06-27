import json

import disnake
from disnake.ext import commands

from utils import error
from utils.sql_manager import readData
from utils.load_lang import economy_lang as langText



class BalanceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /balance has been loaded')

    @commands.slash_command(name="balance", description=langText.get("BALANCE_DESCRIPTION"))
    async def balance(self, ctx):
        try:
            userID = str(ctx.author.id)

            if readData("casinoAccount", userID) == []:
                insertCasinoData((userID, 0))

            casinoAccount = readData("casinoAccount", userID)[0]
            userBalance = casinoAccount[2]

            embed = disnake.Embed(
                title=langText.get("BALANCE_TITLE"),
                description=langText.get("BALANCE_TEXT").format(balance=userBalance),
                color=disnake.Color.blue())

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BalanceCommand(bot))