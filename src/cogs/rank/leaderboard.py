import disnake
from disnake.ext import commands
from utils import error
from utils.load_lang import rank_lang as langText
from utils.sql_manager import executeQuery



class LeaderboardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /leaderboard has been loaded')

    @commands.slash_command(name='leaderboard', description=langText.get("LEADERBOARD_DESCRIPTION"))
    async def leaderboard(self, ctx):
        try:
            query = "SELECT * FROM rankData ORDER BY level DESC, xp DESC"
            sorted_users = executeQuery(query)
            embed = disnake.Embed(
                title=langText.get("LEADERBOARD_TITLE"),
                color=disnake.Color.blurple()
            )
            for i, user_data in enumerate(sorted_users):
                try:
                    user = await self.bot.fetch_user(int(user_data[1]))
                    embed.add_field(
                        name=f"{i+1}. {user.name}",
                        value=langText.get("LEADERBOARD_TEXT").format(userLVL=user_data[3], userXP=user_data[2]),
                        inline=False
                        )
                except disnake.NotFound:
                    pass
                if i == 9:
                    break
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LeaderboardCommand(bot))