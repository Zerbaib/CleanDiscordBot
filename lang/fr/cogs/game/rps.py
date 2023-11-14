import asyncio
import random

import disnake
from disnake.ext import commands

from lang.fr.utils import error


class RPSCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /rps has been loaded')

    @commands.slash_command(name="rps", description="Joue à pierre feuille ciseaux !")
    async def rock_paper_scissors(self, inter: disnake.ApplicationCommandInteraction):
        try:
            choices = {
                0: "Rock",
                1: "Paper",
                2: "Scissors"
            }
            reactions = {
                "🪨": 0,
                "📜": 1,
                "✂️": 2
            }
            embed = disnake.Embed(title="Faite votre choix !")
            embed.color = disnake.Color.blurple()
            embed.set_author(name=inter.author.display_name, icon_url=inter.author.avatar.url)

            # Send the initial embed in the interaction response and store the response
            original_response = await inter.send(embed=embed)
            original_response = await inter.original_response()

            for emoji in reactions:
                await original_response.add_reaction(emoji)

            def check(reaction, user):
                return user == inter.author and str(reaction) in reactions

            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

                user_choice_emote = reaction.emoji
                user_choice_index = reactions[user_choice_emote]

                bot_choice_emote = random.choice(list(reactions.keys()))
                bot_choice_index = reactions[bot_choice_emote]

                result_embed = disnake.Embed()
                result_embed.color = disnake.Color.blurple()
                result_embed.set_author(name=inter.author.display_name, icon_url=inter.author.avatar.url)

                # Use original_response() here without await
                await original_response.clear_reactions()

                if user_choice_index == bot_choice_index:
                    result_embed.description = f"**C'est une égalité !**\nNous avons tous les deux choisi {user_choice_emote}."
                    result_embed.colour = disnake.Color.blurple()
                elif user_choice_index == 0 and bot_choice_index == 2:
                    result_embed.description = f"**Tu as gagné !**\nTu as choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                    result_embed.colour = disnake.Color.brand_green()
                elif user_choice_index == 1 and bot_choice_index == 0:
                    result_embed.description = f"**Tu as gagné !**\nTu as choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                    result_embed.colour = disnake.Color.brand_green()
                elif user_choice_index == 2 and bot_choice_index == 1:
                    result_embed.description = f"**Tu as gagné !**\nTu as choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                    result_embed.colour = disnake.Color.brand_green()
                else:
                    result_embed.description = f"**J'ai gagné !**\nTu as choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                    result_embed.colour = disnake.Color.brand_red()

                # Use original_response() here without await
                await original_response.edit(embed=result_embed)
            except asyncio.exceptions.TimeoutError:
                # Use original_response() here without await
                await original_response.clear_reactions()
                timeout_embed = disnake.Embed(title="Too late", color=disnake.Color.brand_red())
                timeout_embed.set_author(name=inter.author.display_name, icon_url=inter.author.avatar.url)

                # Use original_response() here without await
                await original_response.edit(embed=timeout_embed)
        except Exception as e:
            embed = error.error_embed(e)
            await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(RPSCommand(bot))