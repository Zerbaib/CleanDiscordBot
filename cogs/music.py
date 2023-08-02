import disnake
from disnake.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import asyncio
from utils import error

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.voice = None
        self.spotify = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ Music ⚙️ ==========')
        print('⚠️ 🔩 /play has been loaded ⚠️')
        print('⚠️ 🔩 /skip has been loaded ⚠️')
        print('⚠️ 🔩 /queue has been loaded ⚠️')
        print()

    @commands.Cog.listener()
    async def on_connect(self):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            spotify_client_id = config.get('SPOTIFY_API_ID')
            spotify_client_secret = config.get('SPOTIFY_API_SECRET')

        if spotify_client_id and spotify_client_secret:
            auth_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
            self.spotify = spotipy.Spotify(auth_manager=auth_manager)
        else:
            print("Error: Spotify client ID or client secret not found in config.json")

    @commands.slash_command(name='play', description='Play a song')
    async def play(self, ctx, song: str):
        try:
            if not ctx.author.voice:
                embed = disnake.Embed(
                    title="Error",
                    description="You must be in a voice channel to use this command.",
                    color=disnake.Color.red()
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
                    color=disnake.Color.red()
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

    @commands.slash_command(name='skip', description='Skip the current song')
    async def skip(self, ctx):
        try:
            if self.voice and self.voice.is_playing():
                self.voice.stop()
                await self.play_song(ctx)
            else:
                embed = disnake.Embed(
                    title="Error",
                    description="There is no song currently playing.",
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name='queue', description='Display the song queue')
    async def queue(self, ctx):
        try:
            if not self.queue:
                embed = disnake.Embed(
                    title="Queue",
                    description="The song queue is currently empty.",
                    color=disnake.Color.blurple()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Queue",
                    description="Here is the current song queue:",
                    color=disnake.Color.blurple()
                )
                for i, song in enumerate(self.queue, start=1):
                    embed.add_field(name=f"Song {i}", value=song, inline=False)
                await ctx.response.defer()
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    async def play_song(self, ctx):
        if self.voice and self.voice.is_connected() and self.queue:
            song = self.queue.pop(0)

            embed = disnake.Embed(
                title="Now Playing",
                description=f"Now playing: '{song}'",
                color=disnake.Color.blurple()
            )
            await ctx.send(embed=embed)

            results = self.spotify.search(q=song, limit=1, type='track')
            if results and 'tracks' in results and results['tracks']['items']:
                track = results['tracks']['items'][0]
                url = track['external_urls']['spotify']
                self.voice.play(disnake.FFmpegPCMAudio(url), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.bot.loop))

        else:
            if self.voice:
                await self.voice.disconnect()
                self.voice = None

def setup(bot):
    bot.add_cog(MusicCog(bot))
