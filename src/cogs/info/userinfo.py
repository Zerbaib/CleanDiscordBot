import disnake
from disnake.ext import commands
from utils import error
from utils.load_lang import info_lang as langText



class UserInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /userinfo has been loaded')

    @commands.slash_command(name="userinfo", description=langText.get("USERINFO_DESCRIPTION"))
    async def userinfo(self, ctx, user: disnake.User = None):
        try:
            time = "%H:%M:%S %Y-%m-%d"
            if user is None:
                user = ctx.author

            embed = disnake.Embed(
                title=langText.get("USERINFO_TITLE"),
                color=disnake.Color.blue()
            )
            
            if user.avatar:
                embed.set_thumbnail(url=user.avatar.url)
            else:
                embed.set_thumbnail(url=user.default_avatar.url)
            
            embed.add_field(name=langText.get("USERINFO_NAME"), value=f"```{user.name}```", inline=True)
            
            if user.discriminator != '0':
                embed.add_field(name=langText.get("USERINFO_TAG"), value=f"```{user.discriminator}```", inline=True)
            else:
                embed.add_field(name=langText.get("USERINFO_DISPLAYNAME"), value=f"```{user.display_name}```", inline=True)
            
            embed.add_field(name=langText.get("USERINFO_ID"), value=f"```{user.id}```", inline=False)
            embed.add_field(name=langText.get("USERINFO_BOT"), value=f"```{user.bot}```", inline=True)
            embed.add_field(name=langText.get("USERINFO_CREATED"), value=f"```{user.created_at.strftime(time)}```", inline=True)

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserInfoCommand(bot))