import asyncio

import disnake
from disnake.ext import commands

from data.var import *

status_messages = [
    {"name": "Version", "value": "", "type": disnake.ActivityType.watching},
    {"name": "Users", "value": "", "type": disnake.ActivityType.listening},
    {"name": "Commands", "value": "", "type": disnake.ActivityType.playing},
    {"name": "Love", "value": "", "type": disnake.ActivityType.playing}
]

class StatusUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.update_status())
        print('🧰 Status has been loaded')

    async def update_status(self):
        while True:
            for status in status_messages:
                if status["name"] == "Version":
                    with open(localVersionFilePath, 'r') as version_file:
                        bot_version = version_file.read().strip()
                    status["value"] = f"{bot_version}"
                elif status["name"] == "Users":
                    status["value"] = f"{len(self.bot.users)} users"
                elif status["name"] == "Commands":
                    status["value"] = f"{len(self.bot.slash_commands)} commands"
                elif status["name"] == "Love":
                    status["value"] = f"Love U <3"

            current_status = status_messages.pop(0)
            status_messages.append(current_status)

            await self.bot.change_presence(
                activity=disnake.Activity(
                    type=current_status["type"],
                    name=current_status["value"]
                )
            )
            await asyncio.sleep(4)

def setup(bot):
    bot.add_cog(StatusUtils(bot))
