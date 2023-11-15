import disnake
from disnake.ext import commands

from cogs.utils import error
from cogs.utils.color import hex_to_discord_color
from cogs.utils.embed import create_embed


class UserInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /userinfo has been loaded')

    @commands.slash_command(name="userinfo", description="Get user information")
    async def userinfo(self, ctx, user: disnake.User = None):
        try:
            time = "%H:%M:%S %Y-%m-%d"
            if user is None:
                user = ctx.author

            embed = disnake.Embed(
                title="User Information 👤",
                color=disnake.Color.blue()
            )
            
            if user.avatar:
                embed.set_thumbnail(url=user.avatar.url)
            else:
                embed.set_thumbnail(url=user.default_avatar.url)
            
            embed.add_field(name="Username", value=f"```{user.name}```", inline=True)
            
            if user.discriminator != '0':
                embed.add_field(name="Discriminator", value=f"```{user.discriminator}```", inline=True)
            else:
                embed.add_field(name="Display Name", value=f"```{user.display_name}```", inline=True)
            
            embed.add_field(name="ID", value=f"```{user.id}```", inline=False)
            embed.add_field(name="Bot", value=f"```{user.bot}```", inline=True)
            embed.add_field(name="Created At", value=f"```{user.created_at.strftime(time)}```", inline=True)

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserInfoCommand(bot))