import disnake
from disnake.ext import commands
import json
from utils import error

class OtherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ Other ⚙️ ==========')
        print('🔩 /help has been loaded')
        print('🔩 /ping has been loaded')
        print('🔩 /poll has been loaded')
        print()

    @commands.slash_command(name="help", description="Show the list of available commands")
    async def help(self, ctx):
        try:
            embeds = []
            prefix = self.bot.command_prefix
            if not isinstance(prefix, str):
                prefix = prefix[0]

            for cog_name, cog in self.bot.cogs.items():
                commands = cog.get_commands()
                command_list = [command.name for command in commands]
                command_description = [command.help for command in commands]
                help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))
                
                embed = disnake.Embed(title="Help", description=f"Liste des commandes disponibles dans {cog_name.capitalize()} :", color=0xE8C02A)
                embed.add_field(name="Commandes :", value=f'```{help_text}```', inline=False)
                embeds.append(embed)

            await ctx.response.defer()
            for embed in embeds:
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="ping", description="Get the bot's latency",)
    async def ping(self, ctx):
        try:
            embed = disnake.Embed(
                title=f"🏓 Pong!",
                description=f"The ping is around `{round(self.bot.latency * 1000)}ms` ⏳",
                color=disnake.Color.blurple()
                )
            embed.set_footer(text=f'Command executed by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.response.defer()
            await ctx.send(ephemeral=True, embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="poll", description="Create a poll")
    async def poll(self, ctx, question: str):
        try:
            with open("config.json", 'r') as config_file:
                config = json.load(config_file)
            channel_id = config.get("POLL_ID")

            if not channel_id:
                await ctx.send("Poll channel ID is not specified in the configuration.")
                return

            channel = self.bot.get_channel(channel_id)
            if not channel:
                await ctx.send("Invalid poll channel ID.")
                return

            embed = disnake.Embed(
                title="🗳 New Poll 🗳",
                description=f"```{question}```",
                color=disnake.Color.blurple()
            )
            embed.set_footer(text=f"New poll from {ctx.author}")
            
            message = await channel.send(embed=embed)
            await message.add_reaction("👍")
            await message.add_reaction("⬜️")
            await message.add_reaction("👎")

            await ctx.response.defer()
            await ctx.send("Poll created successfully.", ephemeral=True)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(OtherCog(bot))
