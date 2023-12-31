import json
import os
import random

import disnake
from disnake.ext import commands

from lang.fr.utils import error


class RankCommands(commands.Cog):
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
        print('========== ⚙️ Rank ⚙️ ==========')
        print('🔩 /rank has been loaded')
        print('🔩 /leaderboard has been loaded')
        print()

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
            self.save_data()
            xp_required = 5 * (lvl ** 2) + 10 * lvl + 10
            embed = disnake.Embed(
                title=f'👏 Bravo, {message.author.name}! 👏',
                description=f'**Tu est au niveau **```{lvl}```\n*Il te faut ``{xp_required}`` xp pour le prochain niveau*',
                color=disnake.Color.brand_green()
            )
            
            if 'level_roles' in self.config:
                for level_threshold, role_id in self.config['level_roles'].items():
                    if lvl >= int(level_threshold):
                        role = message.author.guild.get_role(role_id)
                        if role and role not in message.author.roles:
                            await message.author.add_roles(role)
                            embed.add_field(name="Tu viens d'avoir un nouveau role !", value=f"Tu a gagner ✨ {role.mention} ! ✨")
                            self.role_added = True
                        else:
                            self.role_added = False

            msg = await message.channel.send(embed=embed)
            
            if self.role_added == True:
                await msg.delete(delay=15)
            elif self.role_added == False:
                await msg.delete(delay=10)
            else:
                await msg.delete(delay=3)

        self.save_data()

    @commands.slash_command(name='rank', description="Regarde ton rank ou celui d'un autre utilisateur")
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
                    title=f"🔰 {user_name} top -> #{user_rank} 🔰",
                    description=f'**Niveaux:** ```{level}```\n**XP:** ``{xp}``\n*Il te faut* ``{xp_required}`` *pour gagner un niveau*',
                    color=disnake.Color.blurple()
                )

                await inter.response.send_message(embed=embed)
            else:
                await inter.response.send_message(f"{user_name} n'a pas de niveau pour le moment.")
        except Exception as e:
            embed = error.error_embed(e)
            await inter.send(embed=embed)

    @commands.slash_command(name='leaderboard', description="Montre le leaderboard")
    async def leaderboard(self, inter: disnake.ApplicationCommandInteraction):
        try:
            sorted_users = sorted(self.ranks.items(), key=lambda x: (x[1]["level"], x[1]["xp"]), reverse=True)
            embed = disnake.Embed(title="💯 Leaderboard 💯", color=disnake.Color.blurple())
            for i, (user_id, user_data) in enumerate(sorted_users):
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    embed.add_field(name=f"{i+1}. {user.name}", value=f"```Niveaux: {user_data['level']} | XP: {user_data['xp']}```", inline=False)
                except disnake.NotFound:
                    pass
                if i == 9:
                    break
            await inter.send(embed=embed)
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
    bot.add_cog(RankCommands(bot, base_level=1, level_factor=0.1))