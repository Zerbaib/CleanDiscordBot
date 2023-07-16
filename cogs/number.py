import random
import disnake
from disnake.ext import commands

class FindTheNumber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /findnumber has been loaded')
        print('🔩 /guess has been loaded')

    @commands.slash_command(name='findnumber', description="Find the hidden number!")
    async def findnumber(self, ctx):
        if ctx.author.id in self.games:
            embed = disnake.Embed(
                title="Error",
                description="You are already playing a game. Use /guess to make a guess.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            number = random.randint(1, 10000)
            self.games[ctx.author.id] = number

            embed = disnake.Embed(
                title="Find the Number",
                description="I have chosen a number between 1 and 10000. Try to guess it!",
                color=disnake.Color.blurple()
            )
            embed.set_footer(text="Type /guess <number> to make a guess.")
            embed.add_field(name="Instructions:", value="Guess the correct number within the given range.", inline=False)
            embed.add_field(name="Attempts:", value="0/50", inline=False)

            await ctx.send(embed=embed)

    @commands.slash_command(name='guess', description="Guess the number!")
    async def guess(self, ctx, number: int):
        if ctx.author.id not in self.games:
            embed = disnake.Embed(
                title="Error",
                description="You are not currently playing a game. Use /findnumber to start a new game.",
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
                embed.add_field(name="Your Guess:", value=f"{number}", inline=False)
                embed.add_field(name="Correct Number:", value=f"{correct_number}", inline=False)
                del self.games[ctx.author.id]
            elif attempts >= 50:
                embed = disnake.Embed(
                    title="Game Over",
                    description="You have reached the maximum number of attempts.",
                    color=disnake.Color.red()
                )
                embed.add_field(name="Your Guess:", value=f"{number}", inline=False)
                embed.add_field(name="Correct Number:", value=f"{correct_number}", inline=False)
                del self.games[ctx.author.id]
            elif number < correct_number:
                embed = disnake.Embed(
                    title="Too low! ⬆️",
                    description="Try a higher number.",
                    color=disnake.Color.red()
                )
                embed.add_field(name="Your Guess:", value=f"{number}", inline=False)
                embed.add_field(name="Correct Number:", value=f"{correct_number}", inline=False)
                embed.add_field(name="Attempts:", value=f"{attempts}/50", inline=False)
            else:
                embed = disnake.Embed(
                    title="Too high! ⬇️",
                    description="Try a lower number.",
                    color=disnake.Color.red()
                )
                embed.add_field(name="Your Guess:", value=f"{number}", inline=False)
                embed.add_field(name="Correct Number:", value=f"{correct_number}", inline=False)
                embed.add_field(name="Attempts:", value=f"{attempts}/50", inline=False)

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FindTheNumber(bot))