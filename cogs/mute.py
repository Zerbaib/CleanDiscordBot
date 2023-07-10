import disnake
from disnake.ext import commands
import json

class MuteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /mute has been loaded')
        print('🔩 /unmute has been loaded')

    @commands.slash_command(name="mute", description="Mute a member")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: disnake.Member, reason: str = "No reason provided"):
        try:
            with open("config.json", 'r') as config_file:
                config = json.load(config_file)
            role_id = config.get("MUTE_ROLE_ID")
            
            if role_id:
                role = disnake.utils.get(ctx.guild.roles, id=role_id)
                if role:
                    await member.add_roles(role)

            embed = disnake.Embed(
                title="Member Muted",
                description=f"{member.mention} has been muted.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Reason", value=f"```{reason}```")
            await ctx.response.send_message(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title="Error during `/mute`",
                description=f"```{e}```",
                color=disnake.Color.dark_red()
            )
            await ctx.response.send_message(embed=embed)

    @commands.slash_command(name="unmute", description="Unmute a member")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: disnake.Member, reason: str = "No reason provided"):
        try:
            with open("config.json", 'r') as config_file:
                config = json.load(config_file)
            role_id = config.get("MUTE_ROLE_ID")
            
            if role_id:
                role = disnake.utils.get(ctx.guild.roles, id=role_id)
                if role and role in member.roles:
                    await member.remove_roles(role)

            embed = disnake.Embed(
                title="Member Unmuted",
                description=f"{member.mention} has been unmuted.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Reason", value=f"```{reason}```")
            await ctx.response.send_message(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title="Error during `/unmute`",
                description=f"```{e}```",
                color=disnake.Color.dark_red()
            )
            await ctx.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(MuteCommand(bot))
