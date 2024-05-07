import random
import json
import os

import disnake
from disnake.ext import commands

from utils.load_lang import load_rank_lang

langText = load_rank_lang()


def save_data(self):
    with open(self.data_path, 'w') as data_file:
        json.dump(self.ranks, data_file, indent=4)

def load_config(self):
    if os.path.exists(self.config_path):
        with open(self.config_path, 'r') as config_file:
            self.config = json.load(config_file)
    else:
        self.config = {}

class RankSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_path = 'data/ranks.json'
        self.config_path = 'config.json'
        self.config = load_config(self)
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as data_file:
                self.ranks = json.load(data_file)
        else:
            self.ranks = {}
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('⚠️ 🧰 Rank system as been loaded')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        if user_id not in self.ranks:
            self.ranks[user_id] = {"xp": 0, "level": 0}

        self.ranks[user_id]["xp"] += random.randint(1, 5)
        xp = self.ranks[user_id]["xp"]
        lvl = self.ranks[user_id]["level"]

        xp_required = 5 * (lvl ** 2) + 10 * lvl + 10

        if xp >= xp_required:
            lvl = lvl + 1
            self.ranks[user_id]["level"] = lvl
            save_data(self)
            xp_required = 5 * (lvl ** 2) + 10 * lvl + 10
            embed = disnake.Embed(
                title=langText.get("SYS_TITLE").format(userName=message.author.name),
                description=langText.get("SYS_TEXT").format(userLVL=lvl, xpRequired=xp_required),
                color=disnake.Color.brand_green()
            )
            if 'level_roles' in self.config:
                for level_threshold, role_id in self.config['level_roles'].items():
                    if lvl >= int(level_threshold):
                        role = message.author.guild.get_role(role_id)
                        if role and role not in message.author.roles:
                            await message.author.add_roles(role)
                            embed.add_field(name=langText.get("SYS_FIELD_NAME"), value=langText.get("SYS_FIELD_VALUE").format(role=role.mention))
                            role_added = True
                        else:
                            role_added = False

            msg = await message.channel.send(embed=embed)

            if role_added == True:
                await msg.delete(delay=15)
            elif role_added == False:
                await msg.delete(delay=10)
            else:
                await msg.delete(delay=3)

        save_data(self)

def setup(bot):
    bot.add_cog(RankSystem(bot))