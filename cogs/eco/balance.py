import json

import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import load_economy_lang

langText = load_economy_lang()

class BalanceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /balance has been loaded')

    @commands.slash_command(name="balance", description=langText.get("BALANCE_DESCRIPTION"))
    async def balance(self, ctx):
        try:
            user_id = str(ctx.author.id)
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                if user_id not in data:
                    data[user_id] = 0
                    with open(self.data_file, 'w') as file:
                        json.dump(data, file, indent=4)
                balance = data.get(user_id, 0)
            
            embed = disnake.Embed(
                title=langText.get("BALANCE_TITLE"),
                description=langText.get("BALANCE_TEXT").format(balance=balance),
                color=disnake.Color.blue()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BalanceCommand(bot))