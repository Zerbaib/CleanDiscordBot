import disnake
from disnake.ext import commands

class BanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /ban has been loaded')

    @commands.slash_command(name="ban", description="Ban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: disnake.User, reason: str = "No reason provided"):
        try:
            await ctx.guild.ban(user, reason=reason)

            embed = disnake.Embed(
                title="User Banned",
                description=f"**{user.name}** *aka ``{user.display_name}``* has been banned from the server.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Reason", value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)

        except Exception as e:
            embed = disnake.Embed(
                title="Error during `/ban`",
                description=f"```{e}```",
                color=disnake.Color.dark_red()
            )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BanCommand(bot))
