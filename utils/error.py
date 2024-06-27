import disnake



def error_embed(e):
    """
    Create an embed with an error message.

    Parameters:
        title (str): The title of the error embed.
        description (str): The description of the error embed.

    Returns:
        disnake.Embed: The error embed.
    """
    head = "A error as poped !"
    body = f"The exception is\n\n```{e}```"
    issue_link = "https://github.com/Zerbaib/CleanDiscordBot/issues/new?assignees=Zerbaib&labels=bug&projects=&template=bug_report.md&title=%5BBUG%5D"
    embed = disnake.Embed(
        title=head,
        description=body,
        color=disnake.Color.red()
    )
    embed.add_field(
        name="You can now create a Issue on GitHub",
        value=f"Tell us what command and the exeption [**here**]({issue_link})"
    )
    print(f"/n/n{head}\n{body}\n/n/n")
    return embed
