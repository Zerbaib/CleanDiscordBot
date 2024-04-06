import json
import random

import disnake
from disnake.ext import commands

from cogs.utils import error
from cogs.utils.color import hex_to_discord_color
from cogs.utils.embed import create_embed
from cogs.utils.lang_loader import load_casino_lang

langText = load_casino_lang()

class DiceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /dice has been loaded')

    @commands.slash_command(name="dice", description=langText.get("DICE_DESCRIPTION"))
    async def dice(self, ctx, bet: int):
        try:
            user_id = str(ctx.author.id)
            dice_emojis = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:']
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            payout = 0
            
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                bal = data[user_id]
            
            if bet > 0:
                if bet < bal:
                    await ctx.response.defer()
                    if dice1 == dice2:
                        payout = bet * dice1
                        
                        embed = disnake.Embed()
                        embed.title = langText.get("DICE_TITLE")
                        embed.color = disnake.Color.blue()
                        embed.add_field(name=langText.get("DICE_ROLL"), value=f"{dice_emojis[dice1 - 1]}  {dice_emojis[dice2 - 1]}", inline=False)
                        
                        data[user_id] += payout
                        embed.add_field(name=langText.get("OUTCOME_TITLE"), value=langText.get("WIN_DESCRIPTION"))
                        embed.color = disnake.Color.green()
                    else:
                        embed = disnake.Embed()
                        embed.title = langText.get("DICE_TITLE")
                        embed.add_field(name=langText.get("DICE_ROLL"), value=f"{dice_emojis[dice1 - 1]}  {dice_emojis[dice2 - 1]}", inline=False)
                        embed.add_field(name=langText.get("BET"), value=f"`{bet}`")
                        embed.add_field(name=langText.get("OUTCOME_TITLE"), value=langText.get("LOST_OUTCOME"))
                        embed.color = disnake.Color.red()
                        
                        data[user_id] -= bet
                        
                        await ctx.send(embed=embed)
                else:
                    embed = disnake.Embed()
                    embed.title = langText.get("ERROR_TITLE")
                    embed.color = disnake.Color.red()
                    embed.add_field(name="Error", value=langText.get("ERROR_NO_MONEY"))
                    await ctx.send(embed=embed)
            else:
                embed = disnake.Embed()
                embed.title = langText.get("ERROR_TITLE")
                embed.color = disnake.Color.red()
                embed.add_field(name="Error", value=langText.get("ERROR_NEGATIVE_BET"))
                await ctx.send(embed=embed)

            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(DiceCommand(bot))
