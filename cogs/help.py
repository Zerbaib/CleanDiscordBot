import disnake
from disnake.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /help has been loaded')

    @commands.slash_command(name="help", description="Show the list of available commands")
    async def help(self, ctx):
        embed = disnake.Embed(title="Need Help ?", color=disnake.Color.blurple())
        embed.description = f"📚  Welcome to the command list of **{self.bot.user.name}**!\nHere you can find all the available commands and their usage."
        embed.add_field(name="Commands List", value="🔗  To view the list of commands, click [**here**](https://github.com/Zerbaib/CleanDiscordBot/blob/main/CMD.md)", inline=False)
        embed.set_footer(text="Clean Discord Bot", icon_url=self.bot.user.avatar.url)
        await ctx.response.defer()
        await ctx.send(ephemeral=True, embed=embed)

def setup(bot):
    bot.add_cog(HelpCommand(bot))
