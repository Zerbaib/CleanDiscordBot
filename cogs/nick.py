import disnake
from disnake.ext import commands

class NicknameCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /nick has been loaded')

    @commands.slash_command(name="nick", description="Change the nickname of a member")
    async def nick(self, ctx, member: disnake.Member = None, *, nickname: str):
        try:
            if member is None:
                member = ctx.author

            if member == ctx.author or ctx.author.guild_permissions.manage_nicknames:
                if nickname is not None:
                    await member.edit(nick=nickname)

                if nickname is not None:
                    embed = disnake.Embed(
                        title="Nickname Changed",
                        description=f"The nickname of {member.mention} has been changed to ``{nickname}``.",
                        color=disnake.Color.green()
                    )
                else:
                    embed = disnake.Embed(
                        title="No Nickname Specified",
                        description=f"No nickname specified. The nickname remains unchanged.",
                        color=disnake.Color.orange()
                    )
                await ctx.response.defer()
                await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Permission Denied",
                    description="You do not have the permission to change nicknames of other members.",
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)

        except Exception as e:
            embed = disnake.Embed(
                title="Error during `/nick`",
                description=f"```{e}```",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(NicknameCommand(bot))
