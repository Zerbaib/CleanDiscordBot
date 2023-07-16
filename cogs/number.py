import random
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
            await ctx.send("You are already playing a game. Use /guess to make a guess.")
        else:
            # Génère un nombre aléatoire entre 1 et 100
            number = random.randint(1, 100)
            self.games[ctx.author.id] = number
            await ctx.send("I have chosen a number between 1 and 100. Try to guess it!")

    @commands.slash_command(name='guess', description="Guess the number!")
    async def guess(self, ctx, number: int):
        if ctx.author.id not in self.games:
            await ctx.send("You are not currently playing a game. Use /findnumber to start a new game.")
        else:
            correct_number = self.games[ctx.author.id]
            if number == correct_number:
                await ctx.send("Congratulations! You guessed the correct number!")
                del self.games[ctx.author.id]
            elif number < correct_number:
                await ctx.send("Too low! Try a higher number.")
            else:
                await ctx.send("Too high! Try a lower number.")

def setup(bot):
    bot.add_cog(FindTheNumber(bot))
