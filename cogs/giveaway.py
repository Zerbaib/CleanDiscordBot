import random
import asyncio
import json
import disnake
from disnake.ext import commands

# Charger les données de giveaway depuis le fichier data/giveaway.json
def load_giveaway_data():
    try:
        with open("data/giveaway.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Sauvegarder les données de giveaway dans le fichier data/giveaway.json
def save_giveaway_data(data):
    with open("data/giveaway.json", "w") as file:
        json.dump(data, file)

class GiveawayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaways = load_giveaway_data()

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ Giveaway ⚙️ ==========')
        print('🔩 /giveaway has been loaded')
        print()

    @commands.slash_command(name='giveaway', description="Start a giveaway.")
    async def giveaway(self, ctx, prize: str, winners: int, duration: int, unit: str):
        # Vérifier si l'auteur de la commande est un administrateur
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You must be an administrator to start a giveaway.")
            return

        # Vérifier si le nombre de gagnants est valide
        if winners < 1:
            await ctx.send("The number of winners must be at least 1.")
            return

        # Vérifier si l'unité de temps est valide
        time_units = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "D": 86400,
            "M": 2592000,
            "A": 31536000
        }
        if unit not in time_units:
            await ctx.send("Invalid time unit. Use 's' for seconds, 'm' for minutes, 'h' for hours, 'D' for days, 'M' for months, or 'A' for years.")
            return

        # Convertir la durée en secondes
        duration_seconds = duration * time_units[unit]

        # Créer l'embed initial du giveaway
        embed = disnake.Embed(
            title="🎉 Giveaway 🎉",
            description=f"Prize: {prize}\nWinners: {winners}\nReact with 🎉 to enter!\n\nTime remaining: {duration} {unit}",
            color=disnake.Color.blurple()
        )
        embed.set_footer(text=f"Ends in {duration} {unit}")
        giveaway_message = await ctx.channel.send(embed=embed)

        # Ajouter l'emoji 🎉 à l'embed du giveaway
        await giveaway_message.add_reaction("🎉")

        # Enregistrer les données du giveaway
        self.giveaways[giveaway_message.id] = {
            "prize": prize,
            "winners": winners,
            "end_time": ctx.interaction.created_at.timestemp() + duration_seconds,
            "participants": []
        }
        save_giveaway_data(self.giveaways)

        # Planifier la fin du giveaway
        await self.schedule_giveaway_end(giveaway_message.id, duration_seconds)

    async def schedule_giveaway_end(self, message_id, duration_seconds):
        # Vérifier si le giveaway existe dans les données
        if message_id not in self.giveaways:
            return

        giveaway_data = self.giveaways[message_id]

        # Mettre à jour l'embed du giveaway avec le temps restant
        embed = disnake.Embed(
            title="🎉 Giveaway 🎉",
            description=f"Prize: {giveaway_data['prize']}\nWinners: {giveaway_data['winners']}\nReact with 🎉 to enter!\n\nTime remaining: {self.format_time_remaining(duration_seconds)}",
            color=disnake.Color.blurple()
        )
        embed.set_footer(text=f"Ends in {self.format_time_remaining(duration_seconds)}")
        message = await self.bot.fetch_message(message_id)
        await message.edit(embed=embed)

        # Si le temps restant est supérieur à 60 secondes, actualiser l'embed toutes les 60 secondes
        if duration_seconds > 60:
            await asyncio.sleep(60)
            await self.schedule_giveaway_end(message_id, duration_seconds - 60)
        # Si le temps restant est inférieur à 60 secondes mais supérieur à 25 secondes, actualiser l'embed toutes les 10 secondes
        elif duration_seconds > 25:
            await asyncio.sleep(10)
            await self.schedule_giveaway_end(message_id, duration_seconds - 10)
        # Si le temps restant est inférieur à 25 secondes, actualiser l'embed toutes les secondes
        else:
            await asyncio.sleep(1)
            await self.schedule_giveaway_end(message_id, duration_seconds - 1)

        # Une fois que le temps est écoulé, terminer le giveaway
        await self.end_giveaway(message_id)

    async def end_giveaway(self, message_id):
        # Vérifier si le giveaway existe dans les données
        if message_id not in self.giveaways:
            return

        giveaway_data = self.giveaways[message_id]
        winners_count = giveaway_data["winners"]

        # Obtenir tous les participants ayant réagi avec l'emoji 🎉
        message = await self.bot.fetch_message(message_id)
        participants = [user for reaction in message.reactions if str(reaction.emoji) == "🎉" for user in await reaction.users().flatten() if not user.bot]

        # Sélectionner des gagnants au hasard
        winners = random.sample(participants, k=min(winners_count, len(participants)))

        # Envoyer un message privé aux gagnants
        for winner in winners:
            await winner.send(f"Congratulations! You have won the giveaway for {giveaway_data['prize']}!")

        # Mettre à jour l'embed du giveaway avec les gagnants
        embed = message.embeds[0]
        embed.description += f"\n\nWinners:\n" + "\n".join([f"{winner.mention}" for winner in winners])
        await message.edit(embed=embed)

        # Mettre à jour les données du giveaway et sauvegarder
        giveaway_data["participants"] = [user.id for user in participants]
        giveaway_data["winners"] = [winner.id for winner in winners]
        self.giveaways[message_id] = giveaway_data
        save_giveaway_data(self.giveaways)

    def format_time_remaining(self, seconds):
        if seconds >= 3600:
            return f"{seconds // 3600} hours"
        elif seconds >= 60:
            return f"{seconds // 60} minutes"
        else:
            return f"{seconds} seconds"

def setup(bot):
    bot.add_cog(GiveawayCog(bot))
