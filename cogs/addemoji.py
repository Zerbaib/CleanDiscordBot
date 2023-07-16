import disnake
from disnake.ext import commands

class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /addemoji has been loaded')

    @commands.command(name='addemoji')
    @commands.has_permissions(manage_emojis=True)
    async def add_emoji(self, ctx, emoji: disnake.PartialEmoji, name=None):
        if name is None:
            name = emoji.name

        guild = ctx.guild
        try:
            new_emoji = await guild.create_custom_emoji(name=name, image=emoji.url)
            embed = disnake.Embed(
                title='Emoji ajouté',
                description=f"L'emoji {new_emoji} a été ajouté avec succès :tada:",
                color=disnake.Color.green()
            )
            await ctx.send(embed=embed)
        except disnake.HTTPException:
            embed = disnake.Embed(
                title='Erreur',
                description="Une erreur s'est produite lors de l'ajout de l'emoji :x:",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Emoji(bot))
