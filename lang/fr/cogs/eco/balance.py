import json

import disnake
from disnake.ext import commands

from lang.fr.utils import error


class BalanceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /balance has been loaded')
        
    @commands.slash_command(name="balance", description="Regarde ton porte-monnaie")
    async def balance(self, ctx):
        try:
            user_id = str(ctx.author.id)
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                balance = data.get(user_id, 0)
            
            embed = disnake.Embed(
                title="💰 Pore-monnaie 💰",
                description=f"Ton solde: ``{balance}`` pieces 🪙",
                color=disnake.Color.blue()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(BalanceCommand(bot))