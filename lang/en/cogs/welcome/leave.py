import json

import disnake
from disnake.ext import commands


class LeaveMessageUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🧰 Leave has been loaded')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        leave_channel_id = config["LEAVE_ID"]
        leave_channel = self.bot.get_channel(leave_channel_id)
        if leave_channel:
            embed = disnake.Embed(
                title=f"Say goodbye to {member.display_name}",
                description=f"We are sad to see you leave {member.mention}!\n\nWith you, we are now {len(member.guild.members)} members!\n\nWe hope to see you again lat",
                color=disnake.Color.brand_red()
                )
            await leave_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(LeaveMessageUtils(bot))