import os
import json

import disnake
from disnake.ext import commands

from utils import error
from utils.sql_manager import executeQuery
from utils.load_lang import rank_lang as langText
from data.var import *


class LeaderboardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_path = dataFilePath['ranks']
        self.config_path = configFilePath
        self.data = {}
        self.role_added = None
        self.load_data()
        self.load_config()

    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as data_file:
                self.ranks = json.load(data_file)
        else:
            self.ranks = {}

    def save_data(self):
        with open(self.data_path, 'w') as data_file:
            json.dump(self.ranks, data_file, indent=4)

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as config_file:
                self.config = json.load(config_file)
        else:
            self.config = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /leaderboard has been loaded')

    @commands.slash_command(name='leaderboard', description=langText.get("LEADERBOARD_DESCRIPTION"))
    async def leaderboard(self, inter: disnake.ApplicationCommandInteraction):
        try:
            print("3")
            query = "SELECT * FROM rankData ORDER BY level DESC, xp DESC"
            print("3")
            sorted_users = executeQuery(query)
            print("3")
            embed = disnake.Embed(
                title=langText.get("LEADERBOARD_TITLE"),
                color=disnake.Color.blurple()
            )
            print("3")
            for i, user_data in enumerate(sorted_users):
                try:
                    user = await self.bot.fetch_user(int(user_data["user_id"]))
                    embed.add_field(
                        name=f"{i+1}. {user.name}",
                        value=langText.get("LEADERBOARD_TEXT").format(userLVL=user_data["level"], userXP=user_data["xp"]),
                        inline=False
                        )
                except disnake.NotFound:
                    pass
                if i == 9:
                    break
            await inter.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await inter.send(embed=embed)


def setup(bot):
    bot.add_cog(LeaderboardCommand(bot))