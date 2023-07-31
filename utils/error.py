import disnake

def error_embed(title: str, description: str):
    """
    Create an embed with an error message.

    Parameters:
        title (str): The title of the error embed.
        description (str): The description of the error embed.

    Returns:
        disnake.Embed: The error embed.
    """
    issue_link = "https://github.com/Zerbaib/CleanDiscordBot/issues/new"
    embed = disnake.Embed(
        title=title,
        description=description,
        color=disnake.Color.red()
    )
    embed.add_field(
        name="You can now create a Issue on GitHub",
        description=f"Tell us wath command and the exeption [**here**]({issue_link})"
    )
    return embed
