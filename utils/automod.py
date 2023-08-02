import disnake
from disnake.ext import commands
from termcolor import colored
import time
import datetime
import json

class AutoModUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('bad_words.json', 'r') as bad_words_file:
            self.bad_words = json.load(bad_words_file)["bad_words"]

    @commands.Cog.listener()
    async def on_ready(self):
        print('🧰 AutoMod has been loaded')
        print()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            with open('config.json', 'r') as config:
                config = json.load(config)
                      
            content = message.content.lower()

            for word in self.bad_words:
                if word in content:
                    embed = disnake.Embed(
                        title=f"{message.author.display_name} -> {word}",
                        description=f"User has posted a bad word:\n```{word}```",
                        color=disnake.Color.red()
                    )
                    embed.add_field(
                        name="Go to message",
                        value=f"[**`Jump to message`**]({message.jump_url})"
                    )
                    log_channel_id = config["LOG_ID"]
                    log_channel = self.bot.get_channel(log_channel_id)
                    await log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(AutoModUtils(bot))
