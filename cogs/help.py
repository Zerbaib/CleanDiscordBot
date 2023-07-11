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
        embed = disnake.Embed(title="Help menu", color=disnake.Color.blue())

        sorted_commands = sorted(self.bot.slash_commands, key=lambda cmd: cmd.name)

        for command in sorted_commands:
            name = command.name
            description = command.description

            embed.add_field(name=f"/{name}", value=f"```{description}```", inline=False)

        await ctx.response.send_message(ephemeral=True, embed=embed)

def setup(bot):
    bot.add_cog(HelpCommand(bot))
