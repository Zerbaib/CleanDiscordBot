import disnake
from disnake.ext import commands
import json
import os
import random
from utils import error

class RankCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ Join and leave ⚙️ ==========')
        print('🧰 Join has been loaded')
        print('🧰 Leave has been loaded')
        print()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        join_channel_id = config["JOIN_ID"]
        join_channel = self.bot.get_channel(join_channel_id)
        if join_channel:
            embed = disnake.Embed(
                title="Member Joined",
                description=f"{member.mention} has joined the server.",
                color=disnake.Color.brand_green()
                )
            await join_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        leave_channel_id = config["LEAVE_ID"]
        leave_channel = self.bot.get_channel(leave_channel_id)
        if leave_channel:
            embed = disnake.Embed(
                title="Member Left",
                description=f"{member.mention} has left the server.",
                color=disnake.Color.brand_red()
                )
            await leave_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(RankCommands(bot))