import json
import random

import disnake
from disnake.ext import commands

from cogs.utils import error
from cogs.utils.color import hex_to_discord_color
from cogs.utils.embed import create_embed
from cogs.utils.lang_loader import load_casino_lang

langText = load_casino_lang()
discord_blue = "#7289da"
discord_red = "#ed5555"

class BetCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /bet has been loaded')

    @commands.slash_command(name="bet", description=langText.get("BET_DESCRIPTION"))
    async def bet(self, ctx, amount: int):
        try:
            user_id = str(ctx.author.id)
            win_chance = 25
            outcome = random.choices([True, False], weights=[win_chance, 100 - win_chance], k=1)[0]
            with open(self.data_file, 'r+') as file:
                data = json.load(file)
                balance = data.get(user_id, 0)
                if amount > 0:
                    if amount <= balance:
                        if outcome:
                            winnings = amount * 2
                            data[user_id] += winnings
                            embed = disnake.Embed(
                                title=langText.get("WIN_TITLE"),
                                color=hex_to_discord_color(discord_blue)
                                )
                            
                            embed.add_field(
                                name=langText.get('OUTCOME_TITLE'),
                                value=langText.get('WIN_OUTCOME'),
                                inline=False
                                )
                            embed.add_field(
                                name=langText.get('WINNINGS'),
                                value=langText.get("WIN_DESCRIPTION"),
                                inline=False
                                )
                            await ctx.response.defer()
                            await ctx.send(embed=embed)
                        else:
                            data[user_id] -= amount

                            embed = disnake.Embed(
                                title=langText.get('LOST_TITLE'),
                                color=disnake.Color.red()
                                )
                            embed.add_field(
                                name=langText.get('OUTCOME_TITLE'),
                                value=langText.get('LOST_OUTCOME')
                                )
                            await ctx.response.defer()
                            await ctx.send(embed=embed)
                    else:
                        embed = disnake.Embed(
                            title=langText.get('ERROR_TITLE'),
                            color=hex_to_discord_color(discord_red)
                            )
                        embed.add_field(name=langText.get('ERROR_TITLE'), value=langText.get('ERROR_NO_MONEY'))
                        await ctx.response.send_message(embed=embed)
                else:
                    embed = disnake.Embed(
                        title=langText.get('ERROR_TITLE'),
                        color=hex_to_discord_color(discord_red)
                        )
                    embed.add_field(name=langText.get('ERROR_TITLE'), value=langText.get('ERROR_NEGATIVE_BET'))
                    await ctx.response.send_message(embed=embed)
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BetCommand(bot))