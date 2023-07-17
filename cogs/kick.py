import disnake
from disnake.ext import commands

class KickCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /kick has been loaded')

    @commands.slash_command(name="kick", description="Kick a user from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: disnake.Member, reason: str = "No reason provided"):
        try:
            await user.kick(reason=reason)

            embed = disnake.Embed(
                title="User Kicked",
                description=f"**{user.name}** *aka ``{user.display_name}``* has been kicked from the server.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Reason", value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)

        except Exception as e:
            embed = disnake.Embed(
                title="Error during `/kick`",
                description=f"```{e}```",
                color=disnake.Color.dark_red()
            )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(KickCommand(bot))
