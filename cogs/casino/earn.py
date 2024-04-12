import datetime
import json
import random
import time

import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import load_casino_lang

langText = load_casino_lang()

class EarnCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"
        self.cooldown_file = "data/cooldown.json"
        self.cooldown_time = 60 * 60 * 2

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /earn has been loaded')
        
    @commands.slash_command(name="earn", description=langText.get("EARN_DESCRIPTION"))
    async def earn(self, ctx):
        try:
            user_id = str(ctx.author.id)
            current_time = int(time.time())

            with open(self.cooldown_file, 'r') as cooldown_file:
                cooldown_data = json.load(cooldown_file)
                if not cooldown_data:
                    cooldown_data = {}

                last_earn_time = cooldown_data.get(user_id, 0)

                if current_time - last_earn_time >= self.cooldown_time:
                    with open(self.data_file, 'r+') as data_file:
                        try:
                            data = json.load(data_file)
                        except json.JSONDecodeError:
                            data = {}

                        data.setdefault(user_id, 0)

                        earnings = data[user_id] + 100
                        data[user_id] = earnings

                        cooldown_data[user_id] = current_time

                        data_file.seek(0)
                        json.dump(data, data_file, indent=4)

                    with open(self.cooldown_file, 'w') as cooldown_file:
                        cooldown_data[user_id] = current_time
                        json.dump(cooldown_data, cooldown_file, indent=4)

                    
                    embed = disnake.Embed(
                        title=langText.get("EARN_TITLE"),
                        description=langText.get("EARN_TEXT").format(bal=earnings),
                        color=disnake.Color.green()
                    )
                    await ctx.response.defer()
                    await ctx.send(embed=embed)
                else:
                    remaining_time = self.cooldown_time - (current_time - last_earn_time)
                    remaining_time_delta = datetime.timedelta(seconds=remaining_time)
                    remaining_time_str = str(remaining_time_delta)

                    cooldownText = langText.get("EARN_COOLDOWN_DESCRIPTION")
                    formatted_cooldown_text = cooldownText.format(cooldown_time=remaining_time_str)

                    embed = disnake.Embed(
                        title=langText.get("EARN_COOLDOWN_TITLE"),
                        description=formatted_cooldown_text,
                        color=disnake.Color.red()
                    )
                    await ctx.response.defer()
                    await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(EarnCommand(bot))