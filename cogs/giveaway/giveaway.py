import datetime
import random
import asyncio
import json
import disnake
from disnake.ext import commands

from data.var import timeUnits, dataFilePath
from utils.json_manager import load_json, save_json
from utils.load_lang import load_giveaway_lang
from utils import error


langText = load_giveaway_lang()

class GiveawayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaways = load_json(dataFilePath["giveaway"])

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /giveaway has been loaded')

    @commands.slash_command(name='giveaway', description=langText["GIVEAWAY_DESCRIPTION"])
    async def giveaway(self, ctx, prize: str, winners: int, duration: int, unit: str):
        try:
            if ctx.author.bot:
                return

            if not ctx.author.guild_permissions.administrator:
                await ctx.send(langText["ERROR_NOT_ADMIN"])
                return

            # Vérifier si le nombre de gagnants est valide
            if winners < 1:
                await ctx.send(langText["ERROR_WINNER_AMOUNT"])
                return

            # Vérifier si l'unité de temps est valide
            if unit not in timeUnits:
                await ctx.send(langText["ERROR_TIME_UNIT"])
                return

            # Convertir la durée en secondes
            duration_seconds = duration * timeUnits[unit]

            # Créer l'embed initial du giveaway
            embed = disnake.Embed(
                title=langText["GIVEAWAY_TITLE"],
                description=langText["GIVEAWAY_TEXT"].format(prize=prize, winners=winners, duration=duration, unit=unit),
                color=disnake.Color.blurple()
            )
            embed.set_footer(text=langText["GIVEAWAY_FOOTER"].format(timestamp=int(datetime.datetime.now().timestamp() + duration_seconds)))
            giveaway_message = await ctx.channel.send(embed=embed)

            # Ajouter l'emoji 🎉 à l'embed du giveaway
            await giveaway_message.add_reaction("🎉")

            # Enregistrer les données du giveaway
            self.giveaways[giveaway_message.id] = {
                "prize": prize,
                "winners": winners,
                "end_time": giveaway_message.created_at.timestamp() + duration_seconds,
                "participants": []
            }
            save_json(dataFilePath["giveaway"], self.giveaways)

            giveawayMessageID = giveaway_message.id
            
            # Planifier la fin du giveaway
            await self.schedule_giveaway_end(giveawayMessageID, duration_seconds)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    async def schedule_giveaway_end(self, message_id, duration_seconds):
        # Vérifier si le giveaway existe dans les données
        if message_id not in self.giveaways:
            return

        giveaway_data = self.giveaways[message_id]

        prize = giveaway_data["prize"]
        winners = giveaway_data["winners"]
        duration = self.format_time_remaining(duration_seconds)
        unit = "!"
        
        message = self.bot.get_message(message_id)
        embed = message.embeds[0]
        embed.description = langText["GIVEAWAY_TEXT"].format(prize=prize, winners=winners, duration=duration, unit=unit)
        embed.set_footer(text=langText["GIVEAWAY_FOOTER"].format(timestamp=int(datetime.datetime.now().timestamp() + duration_seconds)))
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
        elif duration_seconds > 0:
            await asyncio.sleep(1)
            await self.schedule_giveaway_end(message_id, duration_seconds - 1)
        else:
            await self.end_giveaway(message_id)

    async def end_giveaway(self, message_id):
        # Vérifier si le giveaway existe dans les données
        if message_id not in self.giveaways:
            return

        giveaway_data = self.giveaways[message_id]
        winners_count = giveaway_data["winners"]

        # Obtenir tous les participants ayant réagi avec l'emoji 🎉
        message = self.bot.get_message(message_id)
        participants = [user for reaction in message.reactions if str(reaction.emoji) == "🎉" for user in await reaction.users().flatten() if not user.bot]

        # Sélectionner des gagnants au hasard
        winners = random.sample(participants, k=min(winners_count, len(participants)))

        # Envoyer un message privé aux gagnants
        for winner in winners:
            await winner.send(f"Congratulations! You have won the giveaway for {giveaway_data['prize']}!")

        prize = giveaway_data["prize"]
        winners = "\n".join([winner.mention for winner in winners])

        # Mettre à jour l'embed du giveaway avec les gagnants
        embed = message.embeds[0]
        embed.title = langText["FINISHED_TITLE"]
        embed.description = langText["FINISHED_TEXT"].format(prize=prize)
        embed.description += langText["FINISHED_WINNERS"].format(winners=winners)
        embed.description += f"\n\nWinners:\n" + "\n".join([f"{winner.mention}" for winner in winners])
        embed.set_footer(text="Finish")
        await message.edit(embed=embed)

        # Mettre à jour les données du giveaway et sauvegarder
        giveaway_data["participants"] = [user.id for user in participants]
        giveaway_data["winners"] = [winner.id for winner in winners]
        self.giveaways[message_id] = giveaway_data
        save_json(dataFilePath["giveaway"], self.giveaways)

    def format_time_remaining(self, seconds):
        if seconds >= 86400:
            return f"{seconds // 86400} days"
        elif seconds >= 3600:
            return f"{seconds // 3600} hours"
        elif seconds >= 60:
            return f"{seconds // 60} minutes"
        else:
            return f"{seconds} seconds"

def setup(bot):
    bot.add_cog(GiveawayCog(bot))
