import disnake
from disnake.ext import commands

class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /clear has been loaded')

    @commands.slash_command(name="clear", description="Clear a specified number of messages in the channel")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount)

            embed = disnake.Embed(
                title="Messages Cleared",
                description=f"``{amount}`` messages have been cleared in this channel.",
                color=disnake.Color.dark_green()
            )
            await ctx.response.send_message(ephemeral=True, embed=embed)

        except Exception as e:
            embed = disnake.Embed(
                title="Error during `/clear`",
                description=f"```{e}```",
                color=disnake.Color.dark_red()
            )
            await ctx.response.send_message(ephemeral=True, embed=embed)

def setup(bot):
    bot.add_cog(ClearCommand(bot))
