import disnake



def create_embed(title, description=None):
    """
    Create a discord.Embed object
    
    Parameters:
        title (str): The title of the embed
        description (str): The description of the embed
        
    Returns:
        disnake.Embed: The embed object
    """
    embed = disnake.Embed(
        title=title,
        description=description
        )
    return embed

