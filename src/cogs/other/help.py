import disnake
from disnake.ext import commands
from utils import error
from utils.load_lang import other_lang as langText



class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /help has been loaded')

    @commands.slash_command(name="help", description=langText.get("HELP_DESCRIPTION"))
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

                embed = disnake.Embed(title=langText.get("HELP_TITLE").format(botName=self.bot.user.display_name), description=langText.get("HELP_TEXT"), color=disnake.Color.blurple())
                embed.add_field(name=langText.get("HELP_FIELD").format(cogName=cog_name.capitalize), value=help_text, inline=False)
                embeds.append(embed)
            for embed in embeds:
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCommand(bot))