from disnake.ext import commands

from utils import error
from utils.load_lang import owner_lang as langText
from utils.sql_manager import insertBadWordData



class AddWordCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /stop has been loaded')

    @commands.slash_command(name="addword", description=langText.get("ADDWORD_DESCRIPTION"))
    @commands.is_owner()
    async def stop(self, ctx, badword: str):
        try:
            if badword:
                if badword and ' ' not in badword:
                    insertBadWordData((badword))
                    embed = error.error_embed(f"Added {badword} to the bad word list")
                    await ctx.send(embed=embed)
                else:
                    embed = error.error_embed("Bad word cannot contain spaces")
                    await ctx.send(embed=embed)
            else:
                embed = error.error_embed("No word provided")
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AddWordCommand(bot))
