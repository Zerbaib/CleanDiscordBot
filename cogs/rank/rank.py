import json
import os
import random

import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import load_rank_lang

langText = load_rank_lang()


class RankCommand(commands.Cog):
    def __init__(self, bot, base_level, level_factor):
        self.bot = bot
        self.data_path = 'data/ranks.json'
        self.config_path = 'config.json'
        self.base_level = base_level
        self.level_factor = level_factor
        self.data = {}
        self.role_added = None
        self.load_data()
        self.load_config()

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /rank has been loaded')

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

    @commands.slash_command(name='rank', description=langText.get("RANK_DESCRIPTION"))
    async def rank(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = None):
        try:
            if user is None:
                user_id = str(inter.author.id)
                user_name = str(inter.author.name)
            else:
                user_id = str(user.id)
                user_name = str(user)
            
            if user_id in self.ranks:
                xp = self.ranks[user_id]["xp"]
                level = self.ranks[user_id]["level"]
                xp_required = 5 * (level ** 2) + 10 * level + 10
                user_rank = self.get_user_rank(user_id)
                embed = disnake.Embed(
                    title=langText.get("RANK_TITLE").format(userName=user_name, userRank=user_rank),
                    description=langText.get("RANK_TEXT").format(userLVL=level, userXP=xp, xpRequired=xp_required),
                    color=disnake.Color.blurple()
                )

                await inter.response.send_message(embed=embed)
            else:
                await inter.response.send_message(langText.get("ERROR_NO_RANK_YET").format(userName=user_name))
        except Exception as e:
            embed = error.error_embed(e)
            await inter.send(embed=embed)

    def get_user_rank(self, user_id):
        sorted_ranks = sorted(self.ranks.items(), key=lambda x: (x[1]["level"], x[1]["xp"]), reverse=True)
        for i, (id, _) in enumerate(sorted_ranks):
            if id == user_id:
                return i + 1

        return -1

def setup(bot):
    bot.add_cog(RankCommand(bot, base_level=1, level_factor=0.1))