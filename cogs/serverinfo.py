import disnake
from disnake.ext import commands

class ServerInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /serverinfo has been loaded')

    @commands.slash_command(name="serverinfo", description="Display server information")
    async def serverinfo(self, ctx):
        guild = ctx.guild

        name = guild.name
        logo = guild.icon.url if guild.icon else None
        description = guild.description
        owner = guild.owner
        created_at = guild.created_at
        member_count = guild.member_count
        channel_count = len(guild.channels)
        date = "%d-%m-%Y %H:%M:%S"

        embed = disnake.Embed(title="Server Information", color=disnake.Color.blurple())
        if logo:
            embed.set_thumbnail(url=logo)
        embed.add_field(name="Name", value=f"```{name}```", inline=False)
        if description:
            embed.add_field(name="Description", value=f"```{description}```", inline=False)
        embed.add_field(name="Owner", value=f"{owner.mention}", inline=False)
        embed.add_field(name="Created At", value=f"```{created_at.strftime(date)}```", inline=False)
        embed.add_field(name="Member Count", value=f"```{str(member_count)}```", inline=True)
        embed.add_field(name="Channel Count", value=f"```{str(channel_count)}```", inline=True)

        await ctx.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(ServerInfoCommand(bot))
