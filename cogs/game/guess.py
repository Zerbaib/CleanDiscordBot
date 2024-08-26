import random

import disnake
from disnake.ext import commands
from utils import error
from utils.load_lang import games_lang as langText



class GuessCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /findnumber has been loaded')
        print('🔩 /guess has been loaded')

    @commands.slash_command(name='findnumber', description=langText.get("FINDNUMBER_DESCRIPTION"))
    async def findnumber(self, ctx):
        try:
            if ctx.author.id in self.games:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_EALREADYSTARTED"),
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
                    title=langText.get("FINDNUMBER_TITLE"),
                    description=langText.get("FINDNUMBER_TEXT"),
                    color=disnake.Color.blurple()
                )
                embed.set_footer(langText.get("FINDNUMBER_FOOTER"))
                embed.add_field(name=langText.get("FINDNUMBER_FIELD1_TITLE"), value=langText.get("FINDNUMBER_FIELD1_VALUE"), inline=False)
                embed.add_field(name=langText.get("FINDNUMBER_FIELD2_TITLE"), value=langText.get("FINDNUMBER_FIELD2_VALUE"), inline=False)

                await ctx.response.defer()
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name='guess', description=langText.get("GUESS_DESCRIPTION"))
    async def guess(self, ctx, number: int):
        try:
            if ctx.author.id not in self.games:
                embed = disnake.Embed(
                    title=langText.get("ERROR_TITLE"),
                    description=langText.get("ERROR_NO_GAME"),
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
                        title=langText.get("GUESS_WIN_TITLE"),
                        description=langText.get("GUESS_WIN_TEXT"),
                        color=disnake.Color.green()
                    )
                    embed.add_field(name=langText.get("GUESS_YOUR_GUESS"), value=f"`{number}`", inline=False)
                    embed.add_field(name=langText.get("GUESS_CORRECT_NUMBER"), value=f"``{correct_number}``", inline=False)
                    del self.games[ctx.author.id]
                elif attempts >= 25:
                    embed = disnake.Embed(
                        title=langText.get("GUESS_GAMEOVER_TITLE"),
                        description=langText.get("GUESS_GAMEOVER_TEXT"),
                        color=disnake.Color.red()
                    )
                    embed.add_field(name=langText.get("GUESS_YOUR_GUESS"), value=f"``{number}``", inline=False)
                    embed.add_field(name=langText.get("GUESS_CORRECT_NUMBER"), value=f"`{correct_number}`", inline=False)
                    del self.games[ctx.author.id]
                elif number < correct_number:
                    embed = disnake.Embed(
                        title=langText.get("TOO_LOW_TITLE"),
                        description=langText.get("TOO_LOW_TEXT"),
                        color=disnake.Color.old_blurple()
                    )
                    embed.add_field(name=langText.get("GUESS_YOUR_GUESS"), value=f"``{number}``", inline=False)
                    embed.add_field(name=langText.get("FINDNUMBER_FIELD2_TITLE"), value=f"``{attempts}/25``", inline=False)
                else:
                    embed = disnake.Embed(
                        title=langText.get("TOO_HIGH_TITLE"),
                        description=langText.get("TOO_HIGH_TEXT"),
                        color=disnake.Color.old_blurple()
                    )
                    embed.add_field(name=langText.get("GUESS_YOUR_GUESS"), value=f"``{number}``", inline=False)
                    embed.add_field(name=langText.get("FINDNUMBER_FIELD2_TITLE"), value=f"``{attempts}/25``", inline=False)

                await ctx.response.defer()
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GuessCommands(bot))