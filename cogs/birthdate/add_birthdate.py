import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import casino_lang as langText



class AddBirthdateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /add_birthdate has been loaded')

    @commands.slash_command(name="add_birthdate", description="")
    async def add_birthdate(self, ctx, day: int, mounth: int, year: int = None):
        author = ctx.author
        if author == ctx.author.bot:
            return
        
        if day > 31:
            return
        if mounth > 12:
            return
        

def setup(bot):
    bot.add_cog(AddBirthdateCommand(bot))