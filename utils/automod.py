import json
import re

import disnake
from disnake.ext import commands

from data.var import badWordFilePath, configFilePath


class AutoModUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(badWordFilePath, 'r') as bad_words_file:
            self.bad_words = json.load(bad_words_file)["bad_words"]
            self.bad_word_patterns = [re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE) for word in self.bad_words]
            self.link_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+')
            self.tenor_link = re.compile(r'tenor.com')
            self.media_link = re.compile(r'cdn.discordapp.com')

    @commands.Cog.listener()
    async def on_ready(self):
        print('🧰 AutoMod has been loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if not message.author.guild_permissions.administrator:
                with open(configFilePath, 'r') as config_file:
                    config = json.load(config_file)
                        
                content = message.content.lower()

                for pattern, word in zip(self.bad_word_patterns, self.bad_words):
                    if pattern.search(content):
                        embed = disnake.Embed(
                            title=f"{message.author.display_name} -> {word}",
                            description=f"User has posted a bad word:\n```{word}```",
                            color=disnake.Color.brand_red()
                        )
                        embed.add_field(
                            name="Go to message",
                            value=f"[**`Jump to message`**]({message.jump_url})"
                        )
                        log_channel_id = config["LOG_ID"]
                        log_channel = self.bot.get_channel(log_channel_id)
                        await log_channel.send(embed=embed)
                
                if self.link_pattern.search(message.content):
                    if not self.tenor_link.search(message.content):
                        if not self.media_link.search(message.content):
                            log_channel = self.bot.get_channel(config["LOG_ID"])
                            if log_channel:
                                embed = disnake.Embed(title="Link Detected",
                                                    description=f"A link was fund from {message.author.mention}.",
                                                    color=disnake.Color.brand_red())
                                embed.add_field(name="Message content", value=f"```{message.content}```", inline=False)
                                await log_channel.send(embed=embed)
                            user_embed = disnake.Embed(title="Warning",
                                                    description=f"Your message ```{message.content}``` as been blocked.",
                                                    color=disnake.Color.brand_red())
                            await message.author.send(embed=user_embed)
                            await message.delete()

                            temp_embed = disnake.Embed(
                                description=f"A link as been blocker.\nPlease don't send link {message.author.mention}",
                                color=disnake.Color.brand_red())
                            await message.channel.send(embed=temp_embed, delete_after=10.0)

def setup(bot):
    bot.add_cog(AutoModUtils(bot))
