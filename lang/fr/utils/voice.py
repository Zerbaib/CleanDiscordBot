import asyncio
import json

import disnake
from disnake.ext import commands


class CustomVoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "config.json"
        self.temp_channels = {}
        self.load_config()

    @commands.Cog.listener()
    async def on_ready(self):
        print('🧰 CustomVoice has been loaded')
        print()
        self.bot.loop.create_task(self.delete_temporary_channels())

    def load_config(self):
        with open(self.config_file, 'r') as file:
            self.config = json.load(file)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        target_channel_id = self.config.get('AUTO_VOICE_ID')
        if after.channel and after.channel.id == target_channel_id:
            guild = member.guild
            category = after.channel.category
            overwrites = {
                guild.default_role: disnake.PermissionOverwrite(connect=True),
                member: disnake.PermissionOverwrite(connect=True, manage_channels=True)
            }

            channel = await guild.create_voice_channel(name=member.display_name, overwrites=overwrites, category=category, user_limit=10)
            await member.move_to(channel)

            self.temp_channels[channel.id] = asyncio.get_event_loop().time()

    async def delete_temporary_channels(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            current_time = asyncio.get_event_loop().time()

            for channel_id, creation_time in list(self.temp_channels.items()):
                channel = self.bot.get_channel(channel_id)

                if not channel:
                    del self.temp_channels[channel_id]
                    continue

                if len(channel.members) == 0 and current_time - creation_time >= 3:
                    await channel.delete()
                    del self.temp_channels[channel_id]

            await asyncio.sleep(1)

def setup(bot):
    bot.add_cog(CustomVoiceCog(bot))