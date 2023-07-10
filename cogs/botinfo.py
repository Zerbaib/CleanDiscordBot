import disnake
from disnake.ext import commands

class botinfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /botinfo as been loaded')
    
    @commands.slash_command(name="botinfo", description="Get the bot's info",)
    async def botinfo(self, ctx):
        try:
            embed = disnake.Embed(
                title=f"Info of ``{self.bot.user.name}``",
                description=f"",
                color=disnake.Color.random()
                )
            embed.add_field(
                name=f"Bot profile:",
                value=f"**Name**: ``{self.bot.user.name}``\n"
                      f"**Prefix**: ``{self.bot.command_prefix}``\n"
                      f"**Ping**: "
            )
            embed.set_footer(text=f'Command executed by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.response.send_message(ephemeral=True, embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title=f"Error during the ``/botinfo``",
                description=f"```{e}```",
                color=disnake.Color.red()
                )
            embed.set_footer(text=f'Command executed by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(botinfoCommand(bot))