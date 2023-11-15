import disnake
from disnake.ext import commands

from lang.en.utils import error


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /ping has been loaded')

    @commands.slash_command(name="help", description="Show the list of available commands")
    async def help(self, ctx):
        try:
            embeds = []
            prefix = self.bot.command_prefix
            if not isinstance(prefix, str):
                prefix = prefix[0]

            await ctx.response.defer()
            for cog_name, cog in self.bot.cogs.items():
                commands = cog.get_slash_commands()
                if not commands:
                    continue

                help_text = '\n'.join(f'**`{prefix}{command.name}`** - ```{command.description}```' for command in commands)

                embed = disnake.Embed(title=f"{self.bot.user.display_name} Help", description=f"All command:", color=disnake.Color.blurple())
                embed.add_field(name=f"Commands for {cog_name.capitalize()}", value=help_text, inline=False)
                embeds.append(embed)
            for embed in embeds:
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCommand(bot))