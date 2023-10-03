import disnake
from disnake.ext import commands

from lang.en.utils import error


class ServerInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /serverinfo has been loaded')

    @commands.slash_command(name="serverinfo", description="Display server information")
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

            embed = disnake.Embed(title="💾 Server Information 💾", color=disnake.Color.blurple())
            if logo:
                embed.set_thumbnail(url=logo)
            embed.add_field(name="Name", value=f"```{name}```", inline=False)
            if description:
                embed.add_field(name="Description", value=f"```{description}```", inline=False)
            embed.add_field(name="Owner", value=f"{owner.mention}", inline=False)
            embed.add_field(name="Created At", value=f"```{created_at.strftime(date)}```", inline=False)
            embed.add_field(name="Member Count", value=f"```{str(member_count)}```", inline=True)
            embed.add_field(name="Channel Count", value=f"```{str(channel_count)}```", inline=True)
            embed.add_field(name="Role Count", value=f"```{str(role_count)}```", inline=True)
            embed.add_field(name="Boost Count", value=f"```{str(boost_count)}```", inline=True)
            embed.add_field(name="Boost Tier", value=f"```{str(boost_tier)}```", inline=True)

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ServerInfoCommand(bot))