import disnake
from disnake.ext import commands
import json

class BalanceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /balance has been loaded')

    @commands.slash_command(name="balance", description="Check your balance")
    async def balance(self, ctx):
        user_id = str(ctx.author.id)
        with open(self.data_file, 'r') as file:
            data = json.load(file)
            balance = data.get(user_id, 0)
            if not balance:
                data[user_id] = 0
                balance = 0

        embed = disnake.Embed(
            title="Balance",
            description=f"Your balance: ``{balance}`` coins",
            color=disnake.Color.blue()
        )
        await ctx.response.send_message(embed=embed)

        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

def setup(bot):
    bot.add_cog(BalanceCommand(bot))
