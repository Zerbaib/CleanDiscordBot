import disnake
import asyncio

status_messages = [
    {"name": "Version", "value": "", "type": disnake.ActivityType.watching},
    {"name": "Users", "value": "", "type": disnake.ActivityType.listening},
    {"name": "Commands", "value": "", "type": disnake.ActivityType.playing},
    {"name": "Love", "value": "", "type": disnake.ActivityType.playing}
]

async def update_status(bot):
    print('🧰 status has been loaded')
    while True:
        for status in status_messages:
            if status["name"] == "Version":
                with open('version.txt', 'r') as version_file:
                    bot_version = version_file.read().strip()
                status["value"] = f"{bot_version}"
            elif status["name"] == "Users":
                status["value"] = f"{len(bot.users)} users"
            elif status["name"] == "Commands":
                status["value"] = f"{len(bot.slash_commands)} commands"
            elif status["name"] == "Love":
                status["value"] = f"Love U <3"

        current_status = status_messages.pop(0)
        status_messages.append(current_status)

        await bot.change_presence(
            activity=disnake.Activity(
                type=current_status["type"],
                name=current_status["value"]
            )
        )
        await asyncio.sleep(4)