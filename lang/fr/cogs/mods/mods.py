import json

import aiohttp
import disnake
from disnake.ext import commands

from lang.fr.utils import error


class ModsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /unmute has been loaded')
        print('🔩 /nick has been loaded')
        print('🔩 /kick has been loaded')
        print('🔩 /ban has been loaded')
        print('🔩 /addemoji has been loaded')

    @commands.slash_command(name="unmute", description="Unmute un membre")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: disnake.Member, reason: str = "Aucune raison spécifiée"):
        try:
            with open("config.json", 'r') as config_file:
                config = json.load(config_file)
            role_id = config.get("MUTE_ROLE_ID")

            role = disnake.utils.get(ctx.guild.roles, id=role_id)
            if role and role in member.roles:
                await member.remove_roles(role)

            embed = disnake.Embed(
                title="😐 Membre Démué 😐",
                description=f"{member.mention} a été démuet.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Raison", value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="nick", description="Change le surnom d'un membre")
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
                        title="🥸 Surnom Changé 🥸",
                        description=f"Le surnom de {member.mention} a été changé en ``{nickname}``.",
                        color=disnake.Color.green()
                    )
                else:
                    embed = disnake.Embed(
                        title="Aucun Surnom Spécifié",
                        description=f"Aucun surnom spécifié. Le surnom reste inchangé.",
                        color=disnake.Color.orange()
                    )
                await ctx.response.defer()
                await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Permission Refusée",
                    description="Vous n'avez pas la permission de changer les surnoms des autres membres.",
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="kick", description="Expulse un utilisateur du serveur")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: disnake.Member, reason: str = "Aucune raison spécifiée"):
        try:
            await user.kick(reason=reason)

            embed = disnake.Embed(
                title="🏌️‍♀️ Utilisateur Expulsé 🏌️‍♀️",
                description=f"**{user.name}** *alias ``{user.display_name}``* a été expulsé du serveur.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(name="Raison", value=f"```{reason}```")
            await ctx.response.defer()
            await ctx.send(embed=embed)

        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="ban", description="Bannir un utilisateur du serveur")
    async def ban(self, ctx, user: disnake.User, reason: str = "Aucune raison spécifiée"):
        try:
            member = ctx.guild.get_member(ctx.author.id)
            bot = ctx.guild.get_member(self.bot.user.id)
            if member.guild_permissions.ban_members:
                if bot.guild_permissions.ban_members:
                    await ctx.guild.ban(user, reason=reason)
                    embed = disnake.Embed(
                        title="🔨 Utilisateur Banni 🔨",
                        description=f"**{user.name}** *alias ``{user.display_name}``* a été banni du serveur.",
                        color=disnake.Color.dark_red()
                    )
                    embed.add_field(name="Raison", value=f"`{reason}`")
                    await ctx.response.defer()
                    await ctx.send(embed=embed)
                else:
                    embed = disnake.Embed(
                        title="Erreur",
                        description="Je n'ai pas la permission de bannir les utilisateurs.",
                        color=disnake.Color.red()
                    )
                    await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Erreur",
                    description="Vous n'avez pas la permission de bannir les utilisateurs.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name='addemoji', description="Ajoute un emoji au serveur.")
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