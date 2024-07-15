import json

import disnake
from disnake.ext import commands

from utils import error
from utils.sql_manager import executeQuery
from utils.load_lang import economy_lang as langText



class BaltopCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /baltop has been loaded')

    @commands.slash_command(name="baltop", description=langText.get("BALTOP_DESCRIPTION"))
    async def baltop(self, ctx):
        try:
            query = "SELECT * FROM casinoAccount ORDER BY balance DESC"
            sorted_users = executeQuery(query)

            embed = disnake.Embed(title=langText.get("BALTOP_TITLE"), color=disnake.Color.blurple())
            for idx, user_data in enumerate(sorted_users, start=1):
                user = await self.bot.fetch_user(int(user_data[1]))
                if user:
                    embed.add_field(name=f"{idx}. {user.display_name}", value=langText.get("BALTOP_TEXT").format(balance=user_data[2]), inline=False)
                else:
                    embed.add_field(name=langText.get("BALTOP_NOT_FOUND").format(idx=idx), value=langText.get("BALTOP_TEXT").format(balance=user_data[2]), inline=False)
                if idx == 10:
                    break

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BaltopCommand(bot))