import disnake
from disnake.ext import commands
import json
import aiohttp
from utils import error

class ModsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ Moderation ⚙️ ==========')
        print('🔩 /clear has been loaded')
        print('🔩 /mute has been loaded')
        print('🔩 /unmute has been loaded')
        print('🔩 /nick has been loaded')
        print('🔩 /kick has been loaded')
        print('🔩 /ban has been loaded')
        print('🔩 /addemoji has been loaded')
        print()

    @commands.slash_command(name="clear", description="Clear a specified number of messages in the channel")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount)

            embed = disnake.Embed(
                title="Messages Cleared",
                description=f"``{amount}`` messages have been cleared in this channel.",
                color=disnake.Color.dark_green()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed, ephemeral=True)

        except Exception as e:
            error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="mute", description="Mute a member")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: disnake.Member, reason: str = "No reason provided"):
        try:
            with open("config.json", 'r') as config_file:
                config = json.load(config_file)
            role_id = config.get("MUTE_ROLE_ID")

            role = disnake.utils.get(ctx.guild.roles, id=role_id)
            await member.add_roles(role)

            embed = disnake.Embed(
                title="Member Muted",
                description=f"{member.mention} has been muted.",
                color=disnake.Color.dark_red()
            ) 
            embed.add_field(name="Reason", value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="unmute", description="Unmute a member")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: disnake.Member, reason: str = "No reason provided"):
        try:
            with open("config.json", 'r') as config_file:
                config = json.load(config_file)
            role_id = config.get("MUTE_ROLE_ID")
            
            role = disnake.utils.get(ctx.guild.roles, id=role_id)
            if role and role in member.roles:
                await member.remove_roles(role)

            embed = disnake.Embed(
                title="Member Unmuted",
                description=f"{member.mention} has been unmuted.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Reason", value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="nick", description="Change the nickname of a member")
    async def nick(self, ctx, member: disnake.Member = None, *, nickname: str):
        try:
            if member is None:
                member = ctx.author

            if member == ctx.author or ctx.author.guild_permissions.manage_nicknames:
                if nickname is not None:
                    await member.edit(nick=nickname)

                if nickname is not None:
                    embed = disnake.Embed(
                        title="Nickname Changed",
                        description=f"The nickname of {member.mention} has been changed to ``{nickname}``.",
                        color=disnake.Color.green()
                    )
                else:
                    embed = disnake.Embed(
                        title="No Nickname Specified",
                        description=f"No nickname specified. The nickname remains unchanged.",
                        color=disnake.Color.orange()
                    )
                await ctx.response.defer()
                await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Permission Denied",
                    description="You do not have the permission to change nicknames of other members.",
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)

        except Exception as e:
            error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="kick", description="Kick a user from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: disnake.Member, reason: str = "No reason provided"):
        try:
            await user.kick(reason=reason)

            embed = disnake.Embed(
                title="User Kicked",
                description=f"**{user.name}** *aka ``{user.display_name}``* has been kicked from the server.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Reason", value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)

        except Exception as e:
            error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="ban", description="Ban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: disnake.User, reason: str = "No reason provided"):
        try:
            await ctx.guild.ban(user, reason=reason)

            embed = disnake.Embed(
                title="User Banned",
                description=f"**{user.name}** *aka ``{user.display_name}``* has been banned from the server.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Reason", value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)

        except Exception as e:
            error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name='addemoji', description="Add emoji to the server.")
    @commands.has_permissions(manage_emojis=True)
    async def addemoji(self, ctx, emoji: disnake.PartialEmoji, name=None):
        try:
            if name is None:
                name = emoji.name

            guild = ctx.guild
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(emoji.url)) as resp:
                        if resp.status == 200:
                            image_data = await resp.read()
                            new_emoji = await guild.create_custom_emoji(name=name, image=image_data)
                            embed = disnake.Embed(
                                title='Emoji ajouté',
                                description=f"L'emoji {new_emoji} a été ajouté avec succès :tada:",
                                color=disnake.Color.green()
                            )
                            await ctx.response.defer()
                            await ctx.send(embed=embed)
            except disnake.HTTPException:
                embed = disnake.Embed(
                    title='Erreur',
                    description="Une erreur s'est produite lors de l'ajout de l'emoji :x:",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ModsCog(bot))
