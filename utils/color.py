import disnake

def hex_to_discord_color(hex_color):
    hex_color = hex_color.lstrip('#')
    try:
        return disnake.Color(int(hex_color, 16))
    except:
        return disnake.Color.default()