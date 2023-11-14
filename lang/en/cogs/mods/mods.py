import json

import aiohttp
import disnake
from disnake.ext import commands

from lang.en.utils import error


class ModsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ Moderation ⚙️ ==========')
        print('🔩 /nick has been loaded')
        print('🔩 /kick has been loaded')
        print('🔩 /ban has been loaded')
        print('🔩 /addemoji has been loaded')
        print()

    @commands.slash_command(name="nick", description="Change the nickname of a member")
    async def nick(self, ctx, member: disnake.Member = None, *, nickname: str = None):
        try:
            if member is None:
                member = ctx.author
            if nickname is None:
                nickname = member.name

            if member == ctx.author or ctx.author.guild_permissions.manage_nicknames:
                if nickname is not None:
                    await member.edit(nick=nickname)

                if nickname is not None:
                    embed = disnake.Embed(
                        title="🥸 Nickname Changed 🥸",
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
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="kick", description="Kick a user from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: disnake.Member, reason: str = "No reason provided"):
        try:
            await user.kick(reason=reason)

            embed = disnake.Embed(
                title="🏌️‍♀️ User Kicked 🏌️‍♀️",
                description=f"**{user.name}** *aka ``{user.display_name}``* has been kicked from the server.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Reason", value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="ban", description="Ban a user from the server")
    async def ban(self, ctx, user: disnake.User, reason: str = "No reason provided"):
        try:
            member = ctx.guild.get_member(ctx.author.id)
            bot = ctx.guild.get_member(self.bot.user.id)
            if member.guild_permissions.ban_members:
                if bot.guild_permissions.ban_members:
                    await ctx.guild.ban(user, reason=reason)
                    embed = disnake.Embed(
                        title="🔨 User Banned 🔨",
                        description=f"**{user.name}** *aka ``{user.display_name}``* has been banned from the server.",
                        color=disnake.Color.dark_red()
                        )
                    embed.add_field(name="Reason", value=f"`{reason}`")
                    await ctx.response.defer()
                    await ctx.send(embed=embed)
                else:
                    embed = disnake.Embed(
                        title="Error",
                        description="I don't have the permission to ban users.",
                        color=disnake.Color.red()
                    )
                    await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Error",
                    description="You don't have the permission to ban users.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
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
                                title='✨ Emoji ajouté ✨',
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
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ModsCommands(bot))
