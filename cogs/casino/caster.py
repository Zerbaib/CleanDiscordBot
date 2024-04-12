import json
import random

import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import load_casino_lang

langText = load_casino_lang()

class CasterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"
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
            user_id = str(ctx.author.id)
            bet_option = bet_option.lower()

            if bet_option in self.bet_options:
                if bet_amount > 0:
                    with open(self.data_file, 'r') as file:
                        data = json.load(file)
                        balance = data.get(user_id, 0)
                    if bet_amount < balance:
                        result = random.choice(list(self.bet_options.keys()))
                        resultEmoji = self.bet_options[result]
                        
                        payout = self.payouts.get(bet_option, 0)
                        if result == bet_option:
                            winnings = bet_amount * payout
                            balance += winnings
                            
                            embed = disnake.Embed(
                            title=langText.get("CASTER_TITLE"),
                                description=langText.get("CASTER_WIN_DESCRIPTION").format(result=resultEmoji, winnings=winnings),
                                color=disnake.Color.green()
                            )
                            
                        else:
                            balance -= bet_amount
                            
                            embed = disnake.Embed(
                                title=langText.get("CASTER_TITLE"),
                                description=langText.get("CASTER_LOSE_DESCRIPTION").format(result=resultEmoji),
                                color=disnake.Color.red()
                            )
                            
                        
                        data[user_id] = balance
                        
                        with open(self.data_file, 'w') as file:
                            json.dump(data, file, indent=4)    
                        
                        await ctx.send(embed=embed)
                    else:
                        embed = disnake.Embed(
                            title=langText.get("ERROR_TITLE"),
                            description=langText.get("ERROR_NO_MONEY"),
                            color=disnake.Color.red()
                        )
                    await ctx.send(embed=embed)
                else:
                    embed = disnake.Embed(
                        title=langText.get("ERROR_TITLE"),
                        description=langText.get("ERROR_NEGATIVE_BET"),
                        color=disnake.Color.red()
                    )
                    await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_INVALID_OPTION"),
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CasterCommand(bot))