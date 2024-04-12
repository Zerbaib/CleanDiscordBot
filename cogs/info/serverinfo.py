import disnake
from disnake.ext import commands

from utils import error
from utils.load_lang import load_info_lang

langText = load_info_lang()


class ServerInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /serverinfo has been loaded')

    @commands.slash_command(name="serverinfo", description=langText.get("SRVINFO_DESCRIPTION"))
    async def serverinfo(self, ctx):
        try:
            guild = ctx.guild

            name = guild.name
            logo = guild.icon.url if guild.icon else None
            description = guild.description
            owner = guild.owner
            created_at = guild.created_at
            member_count = guild.member_count
            channel_count = len(guild.channels)
            role_count = len(guild.roles)
            boost_count = guild.premium_subscription_count
            boost_tier = guild.premium_tier
            date = "%d-%m-%Y %H:%M:%S"

            embed = disnake.Embed(title=langText.get("SRVINFO_TITLE"), color=disnake.Color.blurple())
            if logo:
                embed.set_thumbnail(url=logo)
            embed.add_field(name=langText.get("SRVINFO_NAME"), value=f"```{name}```", inline=False)
            if description:
                embed.add_field(name=langText.get("SRVINFO_DESC"), value=f"```{description}```", inline=False)
            embed.add_field(name=langText.get("SRVINFO_OWNER"), value=f"{owner.mention}", inline=False)
            embed.add_field(name=langText.get("SRVINFO_CREATED"), value=f"```{created_at.strftime(date)}```", inline=False)
            embed.add_field(name=langText.get("SRVINFO_MEMBERS"), value=f"```{str(member_count)}```", inline=True)
            embed.add_field(name=langText.get("SRVINFO_CHANNELS"), value=f"```{str(channel_count)}```", inline=True)
            embed.add_field(name=langText.get("SRVINFO_ROLES"), value=f"```{str(role_count)}```", inline=True)
            embed.add_field(name=langText.get("SRVINFO_BOOSTS"), value=f"```{str(boost_count)}```", inline=True)
            embed.add_field(name=langText.get("SRVINFO_BOOSTS_TIER"), value=f"```{str(boost_tier)}```", inline=True)

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ServerInfoCommand(bot))