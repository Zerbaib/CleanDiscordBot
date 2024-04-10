import json

import disnake
from disnake.ext import commands

from lang.en.utils import error

class BaltopCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /baltop has been loaded')

    @commands.slash_command(name="baltop", description="Top 10 richest users")
    async def baltop(self, ctx):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)

            sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)
            top_users = sorted_data[:10]

            embed = disnake.Embed(title="💰 Top 10 Richest Users 💰", color=disnake.Color.blurple())
            for idx, (user_id, balance) in enumerate(top_users, start=1):
                user = self.bot.get_user(int(user_id))
                if user:
                    embed.add_field(name=f"{idx}. {user.display_name}", value=f"Balance: `{balance}` coins", inline=False)
                else:
                    embed.add_field(name=f"{idx}. User Not Found", value=f"Balance: `{balance}` coins", inline=False)

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BaltopCommand(bot))