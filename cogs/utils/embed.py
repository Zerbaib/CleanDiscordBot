import disnake
from datetime import datetime

def create_embed(title, description=None):
    embed = disnake.Embed(
        title=title,
        description=description
        )
    return embed

