import json

import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import economy_lang

langText = economy_lang


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
            if amount <= 0:
                embed = disnake.Embed(
                    title=langText.get("ERROR_INVALID_AMOUNT_TITLE"),
                    description=langText.get("ERROR_INVALID_AMOUNT_DESCRIPTION"),
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
                return

            if user.bot:
                embed = disnake.Embed(
                    title=langText.get("ERROR_INVALID_USER_TITLE"),
                    description=langText.get("ERROR_INVALID_USER_DESCRIPTION"),
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
                return

            sender_id = str(ctx.author.id)
            recipient_id = str(user.id)

            with open(self.data_file, 'r') as file:
                data = json.load(file)
                sender_balance = data.get(sender_id, 0)

            if sender_balance < amount:
                embed = disnake.Embed(
                    title=langText.get("ERROR_INSUFFICIENT_FUNDS_TITLE"),
                    description=langText.get("ERROR_INSUFFICIENT_FUNDS_DESCRIPTION"),
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
                return

            with open(self.data_file, 'r+') as file:
                data = json.load(file)
                sender_balance -= amount
                recipient_balance = data.get(recipient_id, 0)
                recipient_balance += amount

                data[sender_id] = sender_balance
                data[recipient_id] = recipient_balance

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

            embed = disnake.Embed(
                title=langText.get("PAY_TITLE"),
                description=langText.get("PAY_DESCRIPTION").format(amount=amount, user=user.mention),
                color=disnake.Color.green()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(PayCommand(bot))
