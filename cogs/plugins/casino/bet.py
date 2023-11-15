import i18n
import os
import json
import random

import disnake
from disnake.ext import commands

from cogs.utils import error
from cogs.utils.color import hex_to_discord_color
from cogs.utils.embed import create_embed

lang = os.environ["LANGUAGE"]
discord_blue = "#7289da"
discord_red = "#ed5555"

class BetCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /bet has been loaded')

    @commands.slash_command(name="bet", description=i18n.t('casino.BET_DESCRIPTION', locale=lang))
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
                            embed = create_embed(i18n.t('casino.WIN_TITLE', locale=lang))
                            embed.color(hex_to_discord_color(discord_blue))
                            
                            embed.add_field(
                                name=i18n.t('casino.OUTCOME_TITLE', locale=lang),
                                value=i18n.t('casino.WIN_OUTCOME', locale=lang),
                                inline=False
                                )
                            embed.add_field(
                                name=i18n.t('casino.WINNINGS', locale=lang),
                                value=i18n.t("casino.WIN_DESCRIPTION", locale=lang, win_bet=winnings),
                                inline=False
                                )
                            await ctx.response.defer()
                            await ctx.send(embed=embed)
                        else:
                            data[user_id] -= amount
                            embed = disnake.Embed(
                                title=i18n.t('casino.LOST_TITLE', locale=lang),
                                color=disnake.Color.red()
                                )
                            embed.add_field(
                                name=i18n.t('casino.OUTCOME_TITLE', locale=lang),
                                value=i18n.t('casino.LOST_OUTCOME', locale=lang)
                                )
                            await ctx.response.defer()
                            await ctx.send(embed=embed)
                    else:
                        embed = create_embed(i18n.t('casino.ERROR_TITLE', locale=lang))
                        embed.color(hex_to_discord_color(discord_red))
                        embed.add_field(name=i18n.t('casino.ERROR_TITLE', local=lang), value=i18n.t('casino.ERROR_NO_MONEY', local=lang))
                        await ctx.response.send_message(embed=embed)
                else:
                    embed = create_embed(i18n.t('casino.ERROR_TITLE', locale=lang))
                    embed.color(hex_to_discord_color(discord_red))
                    embed.add_field(name=i18n.t('casino.ERROR_TITLE', local=lang), value=i18n.t('casino.ERROR_NEGATIVE_BET', local=lang))
                    await ctx.response.send_message(embed=embed)
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BetCommand(bot))