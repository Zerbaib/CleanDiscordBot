import disnake
from disnake.ext import commands

from lang.en.utils import error


class LeaderboardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /leaderboard has been loaded')

    @commands.slash_command(name='leaderboard', description='Show the top 10 xp leaderboard')
    async def leaderboard(self, inter: disnake.ApplicationCommandInteraction):
        try:
            sorted_users = sorted(self.ranks.items(), key=lambda x: (x[1]["level"], x[1]["xp"]), reverse=True)
            embed = disnake.Embed(title="💯 Leaderboard 💯", color=disnake.Color.blurple())
            for i, (user_id, user_data) in enumerate(sorted_users):
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    embed.add_field(name=f"{i+1}. {user.name}", value=f"```Level: {user_data['level']} | XP: {user_data['xp']}```", inline=False)
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
    bot.add_cog(LeaderboardCommand(bot))