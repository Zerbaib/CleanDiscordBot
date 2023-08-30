import random
import asyncio
import disnake
from disnake.ext import commands
from utils import error

class GameCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ Game ⚙️ ==========')
        print('===== 🔗 Numbers')
        print('🔩 /findnumber has been loaded')
        print('🔩 /guess has been loaded')
        print('===== 🔗 Rock Paper Scissors')
        print('🔩 /rps has been loaded')
        print()

    @commands.slash_command(name='findnumber', description="Find the hidden number!")
    async def findnumber(self, ctx):
        try:
            if ctx.author.id in self.games:
                embed = disnake.Embed(
                    title="Error",
                    description="You are already playing a game. Use ``/guess`` to make a guess.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
            else:
                number = random.randint(1, 10000)
                self.games[ctx.author.id] = {
                    "number": number,
                    "attempts": 0
                }

                embed = disnake.Embed(
                    title="Find the Number",
                    description="I have chosen a number between ``1`` and ``10000``. Try to guess it!",
                    color=disnake.Color.blurple()
                )
                embed.set_footer(text="Type ``/guess <number>`` to make a guess.")
                embed.add_field(name="Instructions:", value="Guess the correct number within the given range.", inline=False)
                embed.add_field(name="Attempts:", value="``0/25``", inline=False)

                await ctx.response.defer()
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name='guess', description="Guess the number!")
    async def guess(self, ctx, number: int):
        try:
            if ctx.author.id not in self.games:
                embed = disnake.Embed(
                    title="Error",
                    description="You are not currently playing a game. Use **``/findnumber``** to start a new game.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
            else:
                game = self.games[ctx.author.id]
                correct_number = game["number"]
                attempts = game["attempts"] + 1
                self.games[ctx.author.id]["attempts"] = attempts

                if number == correct_number:
                    embed = disnake.Embed(
                        title="Congratulations! 🎉",
                        description="You guessed the correct number!",
                        color=disnake.Color.green()
                    )
                    embed.add_field(name="Your Guess:", value=f"`{number}`", inline=False)
                    embed.add_field(name="Correct Number:", value=f"``{correct_number}``", inline=False)
                    del self.games[ctx.author.id]
                elif attempts >= 25:
                    embed = disnake.Embed(
                        title="Game Over",
                        description="You have reached the maximum number of attempts.",
                        color=disnake.Color.red()
                    )
                    embed.add_field(name="Your Guess:", value=f"``{number}``", inline=False)
                    embed.add_field(name="Correct Number:", value=f"`{correct_number}`", inline=False)
                    del self.games[ctx.author.id]
                elif number < correct_number:
                    embed = disnake.Embed(
                        title="Too low! ⬆️",
                        description="Try a higher number.",
                        color=disnake.Color.old_blurple()
                    )
                    embed.add_field(name="Your Guess:", value=f"``{number}``", inline=False)
                    embed.add_field(name="Attempts:", value=f"``{attempts}/25``", inline=False)
                else:
                    embed = disnake.Embed(
                        title="Too high! ⬇️",
                        description="Try a lower number.",
                        color=disnake.Color.old_blurple()
                    )
                    embed.add_field(name="Your Guess:", value=f"``{number}``", inline=False)
                    embed.add_field(name="Attempts:", value=f"``{attempts}/25``", inline=False)

                await ctx.response.defer()
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="rps", description="Play rock-paper-scissors versus the bot.")
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
            embed = disnake.Embed(title="Set your choice, please.")
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
                    result_embed.description = f"**It's a tie!**\nYou chose {user_choice_emote} and I chose {bot_choice_emote}."
                    result_embed.colour = disnake.Color.blurple()
                elif user_choice_index == 0 and bot_choice_index == 2:
                    result_embed.description = f"**You won!**\nYou chose {user_choice_emote} and I chose {bot_choice_emote}."
                    result_embed.colour = disnake.Color.brand_green()
                elif user_choice_index == 1 and bot_choice_index == 0:
                    result_embed.description = f"**You won!**\nYou chose {user_choice_emote} and I chose {bot_choice_emote}."
                    result_embed.colour = disnake.Color.brand_green()
                elif user_choice_index == 2 and bot_choice_index == 1:
                    result_embed.description = f"**You won!**\nYou chose {user_choice_emote} and I chose {bot_choice_emote}."
                    result_embed.colour = disnake.Color.brand_green()
                else:
                    result_embed.description = f"**I won!**\nYou chose {user_choice_emote} and I chose {bot_choice_emote}."
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
    bot.add_cog(GameCommands(bot))