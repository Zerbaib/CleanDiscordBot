import disnake
from disnake.ext import commands
import json

class WelcomeCog(commands.Cog):
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
                title=f"Say welcome to {member.display_name}!",
                description=f"We are happy to have you here **{member.mention}**!\n\nWith you, we are now `{len(member.guild.members)}` members!\n\nBe **happy** and **enjoy** your stay !",
                color=disnake.Color.blurple()
                )
            msg = await join_channel.send(embed=embed)
            await msg.add_reaction("👋")

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
    bot.add_cog(WelcomeCog(bot))