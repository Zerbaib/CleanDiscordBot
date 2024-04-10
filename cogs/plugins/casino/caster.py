import json
import random

import disnake
from disnake.ext import commands

from cogs.utils import error
from cogs.utils.lang_loader import load_casino_lang

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
                        payout = self.payouts.get(bet_option, 0)
                        if result == bet_option:
                            winnings = bet_amount * payout
                            balance += winnings
                            
                            casterDescription = langText.get("CASTER_WIN_DESCRIPTION")
                            formatted_caster_description = casterDescription.format(result=self.bet_options[result], winnings=winnings)
                            
                            embed = disnake.Embed(
                            title=langText.get("CASTER_TITLE"),
                                description=formatted_caster_description,
                                color=disnake.Color.green()
                            )
                        else:
                            balance -= bet_amount
                            
                            casterDescription = langText.get("CASTER_LOSE_DESCRIPTION")
                            formatted_caster_description = casterDescription.format(result=self.bet_options[result])
                            
                            embed = disnake.Embed(
                                title=langText.get("CASTER_TITLE"),
                                description=formatted_caster_description,
                                color=disnake.Color.red()
                            )
                        
                        data[user_id] = balance
                        
                        with open(self.data_file, 'w') as file:
                            json.dump(data, file, indent=4)    
                        
                        await ctx.response.defer()
                        await ctx.send(embed=embed)
                    else:
                        embed = disnake.Embed(
                            title=langText.get("ERROR_TITLE"),
                            description=langText.get("ERROR_NO_MONEY"),
                            color=disnake.Color.red()
                        )
                    await ctx.response.send_message(embed=embed)
                else:
                    embed = disnake.Embed(
                        title=langText.get("ERROR_TITLE"),
                        description=langText.get("ERROR_NEGATIVE_BET"),
                        color=disnake.Color.red()
                    )
                    await ctx.response.send_message(embed=embed)
            else:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_INVALID_OPTION"),
                    color=disnake.Color.red()
                )
                await ctx.response.send_message(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CasterCommand(bot))