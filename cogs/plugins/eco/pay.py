import json

import disnake
from disnake.ext import commands

from cogs.utils import error
from cogs.utils.color import hex_to_discord_color
from cogs.utils.embed import create_embed


class PayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /pay has been loaded')

    @commands.slash_command(name="pay", description="Give coins to another user")
    async def pay(self, ctx, amount: int, user: disnake.Member):
        try:
            if amount <= 0:
                embed = disnake.Embed(
                    title="Invalid Amount",
                    description="The amount must be greater than zero.",
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
                return

            if user.bot:
                embed = disnake.Embed(
                    title="Invalid User",
                    description="You cannot give coins to a bot.",
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
                    title="Insufficient Balance",
                    description="You do not have enough coins to make this transaction.",
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
                title="💸 Coins Transferred 💸",
                description=f"You have successfully transferred `{amount}` coins to {user.mention}.",
                color=disnake.Color.green()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(PayCommand(bot))
