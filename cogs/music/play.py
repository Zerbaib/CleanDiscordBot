import disnake
from disnake.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import asyncio

from utils import error


class PlayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.voice = None
        self.spotify = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('⚠️ 🔩 /play has been loaded ⚠️')
    
    @commands.slash_command(name='play', description='Play a song')
    async def play(self, ctx, song: str):
        try:
            if not ctx.author.voice:
                embed = disnake.Embed(
                    title="Error",
                    description="You must be in a voice channel to use this command.",
                    color=disnake.Color.brand_red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
                return

            voice_channel = ctx.author.voice.channel

            if self.voice is None or not self.voice.is_connected():
                self.voice = await voice_channel.connect()
            elif self.voice.channel != voice_channel:
                embed = disnake.Embed(
                    title="Error",
                    description="I'm already playing music in another voice channel.",
                    color=disnake.Color.brand_red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
                return

            self.queue.append(song)

            if self.voice.is_playing():
                embed = disnake.Embed(
                    title="Song Added",
                    description=f"The song '{song}' has been added to the queue.",
                    color=disnake.Color.blurple()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
            else:
                await self.play_song(ctx)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(PlayCommand(bot))