import disnake
import datetime
from lang.fr.utils.logger import log_writer

def error_embed(e):
    """
    Créer un embed pour afficher un message d'erreur.

    Paramètres :
        e (str) : L'exception ou l'erreur à afficher.

    Renvoie :
        disnake.Embed : L'embed d'erreur.
    """
    head = "Une erreur s'est produite !"
    body = f"L'exception est\n\n```{e}```"
    issue_link = "https://github.com/Zerbaib/CleanDiscordBot/issues/new?assignees=Zerbaib&labels=bug&projects=&template=bug_report.md&title=%5BBUG%5D"
    embed = disnake.Embed(
        title=head,
        description=body,
        color=disnake.Color.red()
    )
    embed.add_field(
        name="Vous pouvez maintenant créer un ticket sur GitHub",
        value=f"Dites-nous quelle commande a provoqué cette exception [**ici**]({issue_link})"
    )
    print(f"\n\n{head}\n{body}\n\n")
    return embed
