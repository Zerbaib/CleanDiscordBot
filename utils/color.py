import disnake

def hex_to_discord_color(hex_color):
    """
    Convert a hex color to a discord.Color object

    Parameters:
        hex_color (str): The hex color to convert

    Returns:
        disnake.Color: The discord.Color object
    """

    hex_color = hex_color.lstrip('#')
    try:
        return disnake.Color(int(hex_color, 16))
    except:
        return disnake.Color.default()