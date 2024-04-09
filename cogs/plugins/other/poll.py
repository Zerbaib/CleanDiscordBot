import json

import disnake
from disnake.ext import commands

from cogs.utils import error
from cogs.utils.color import hex_to_discord_color
from cogs.utils.embed import create_embed
from cogs.utils.lang_loader import load_other_lang

langText = load_other_lang()


class PollCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /poll has been loaded')

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
            await message.add_reaction("⬜")
            await message.add_reaction("👎")

            await ctx.response.defer()
            await ctx.send("Poll created successfully.", ephemeral=True)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(PollCommand(bot))