import json
import os
import random

import disnake
from disnake.ext import commands

from utils import error
from utils.sql_manager import readData, connectDB, insertRankData
from utils.load_lang import rank_lang as langText
from utils.xp_required import xp_required_calc

class RankCommand(commands.Cog):
    def __init__(self, bot, base_level, level_factor):
        self.bot = bot
        self.data_path = 'data/ranks.json'
        self.config_path = 'config.json'
        self.base_level = base_level
        self.level_factor = level_factor
        self.load_config()

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /rank has been loaded')

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as config_file:
                self.config = json.load(config_file)
        else:
            self.config = {}

    @commands.slash_command(name='rank', description=langText.get("RANK_DESCRIPTION"))
    async def rank(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = None):
        try:
            if user is None:
                userID = int(inter.author.id)
                userName = str(inter.author.name)
            else:
                userID = int(user.id)
                userName = str(user)

            if readData("rankData", userID) == []:
                insertRankData((userID, 0, 0))

            ranksData = readData("rankData", userID)[0]
            xp = ranksData[2]
            level = ranksData[3]
            xp_required = xp_required_calc(level)
            user_rank = self.get_user_rank(userID)

            embed = disnake.Embed(
                title=langText.get("RANK_TITLE").format(userName=userName, userRank=user_rank),
                description=langText.get("RANK_TEXT").format(userLVL=level, userXP=xp, xpRequired=xp_required),
                color=disnake.Color.blurple()
            )

            await inter.response.send_message(embed=embed)
        except Exception as e:
            print(f"Error in /rank command: {e}")
            embed = error.error_embed(e)
            await inter.response.send_message(embed=embed)

    def get_user_rank(self, userID):
        query = "SELECT * FROM rankData ORDER BY level DESC, xp DESC"
        result = self.execute_query(query)
        for i, row in enumerate(result):
            if row[0] == userID:
                return i + 1
        return -1

    def execute_query(self, query):
        try:
            conn, cur = connectDB()
            cur.execute(query)
            result = cur.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

def setup(bot):
    bot.add_cog(RankCommand(bot, base_level=1, level_factor=0.1))
