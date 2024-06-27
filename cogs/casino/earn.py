import datetime
import json
import random
import time

import disnake
from disnake.ext import commands

from utils import error
from data.var import cooldownTime
from utils.sql_manager import insertCasinoData, updateCasinoData, insertCooldownData, updateCooldownData, readData
from utils.load_lang import casino_lang as langText



class EarnCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"
        self.cooldown_file = "data/cooldown.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /earn has been loaded')

    @commands.slash_command(name="earn", description=langText.get("EARN_DESCRIPTION"))
    async def earn(self, ctx):
        try:
            user_id = str(ctx.author.id)
            current_time = int(time.time())

            if readData("cooldownTime", user_id) == []:
                insertCooldownData((user_id, 0))
                pass
            if readData("casinoAccount", user_id) == []:
                insertCasinoData((user_id, 0))
                pass

            cooldownData = readData("cooldownTime", user_id)[0]
            casinoData = readData("casinoAccount", user_id)[0]
            last_earn_time = cooldownData[2]

            if current_time - last_earn_time >= cooldownTime:
                newBalance = casinoData[2] + 100

                updateCooldownData((user_id, current_time))
                updateCasinoData((user_id, newBalance))

                embed = disnake.Embed(
                    title=langText.get("EARN_TITLE"),
                    description=langText.get("EARN_TEXT").format(bal=newBalance),
                    color=disnake.Color.green())
                pass
            else:
                remaining_time = cooldownTime - (current_time - last_earn_time)
                remaining_time_delta = datetime.timedelta(seconds=remaining_time)
                remaining_time_str = str(remaining_time_delta)

                cooldownText = langText.get("EARN_COOLDOWN_DESCRIPTION")
                formatted_cooldown_text = cooldownText.format(cooldown_time=remaining_time_str)

                embed = disnake.Embed(
                    title=langText.get("EARN_COOLDOWN_TITLE"),
                    description=formatted_cooldown_text,
                    color=disnake.Color.red())
                pass

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(EarnCommand(bot))