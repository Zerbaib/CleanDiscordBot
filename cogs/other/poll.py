import json

import disnake
from disnake.ext import commands
from utils import error
from utils.load_lang import other_lang as langText



class PollCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /poll has been loaded')

    @commands.slash_command(name="poll", description=langText.get("POLL_DESCRIPTION"))
    async def poll(self, ctx, question: str):
        try:
            with open("config.json", 'r') as config_file:
                config = json.load(config_file)
            channel_id = config.get("POLL_ID")

            if not channel_id:
                await ctx.send(langText.get("POLL_NOID"))
                return

            channel = self.bot.get_channel(channel_id)
            if not channel:
                await ctx.send(langText.get("POLL_INVALIDID"))
                return

            embed = disnake.Embed(
                title=langText.get("POLL_TITLE"),
                description=f"```{question}```",
                color=disnake.Color.blurple()
            )
            embed.set_footer(text=langText.get("POLL_FOOTER").format(author=ctx.author))
            
            message = await channel.send(embed=embed)
            await message.add_reaction("👍")
            await message.add_reaction("⬜")
            await message.add_reaction("👎")

            await ctx.response.defer()
            await ctx.send(langText.get("POLL_CREATED_SUCCESS"), ephemeral=True)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(PollCommand(bot))