import disnake
from disnake.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import youtube_dl
import asyncio
from collections import deque

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = deque()
        self.voice = None
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /play has been loaded')
        print('🔩 /skip has been loaded')
        print('🔩 /queue has been loaded')

    @commands.slash_command(name='play', description='Play a song')
    async def play(self, ctx, song: str):
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

        # Use spotipy to search for the song on Spotify
        results = self.spotify.search(q=song, type='track')
        if len(results['tracks']['items']) > 0:
            track = results['tracks']['items'][0]
            artist = track['artists'][0]['name']
            track_name = track['name']
            youtube_link = self.get_youtube_link(artist, track_name)
            if youtube_link:
                self.queue.append(youtube_link)
                if self.voice.is_playing():
                    embed = disnake.Embed(
                        title="Song Added",
                        description=f"The song '{track_name}' by '{artist}' has been added to the queue.",
                        color=disnake.Color.blurple()
                    )
                    await ctx.response.defer()
                    await ctx.send(embed=embed)
                else:
                    await self.play_song(ctx)
            else:
                embed = disnake.Embed(
                    title="Error",
                    description="Failed to retrieve the YouTube link for the song.",
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
        else:
            embed = disnake.Embed(
                title="Error",
                description="No results found for the specified song.",
                color=disnake.Color.red()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed)

    # Helper function to get the YouTube link for a song
    def get_youtube_link(self, artist, track_name):
        query = f"{artist} {track_name} official audio"
        ydl_opts = {
            'format': 'bestaudio/best',
            'default_search': 'auto',
            'quiet': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info:
                    # Take the first video from the search results
                    video_url = info['entries'][0]['webpage_url']
                    return video_url
            except youtube_dl.DownloadError as e:
                print(f"Error extracting YouTube link: {e}")
        return None

    @commands.slash_command(name='skip', description='Skip the current song')
    async def skip(self, ctx):
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

    @commands.slash_command(name='queue', description='Display the song queue')
    async def queue(self, ctx):
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

    async def play_song(self, ctx):
        if self.queue:
            song = self.queue.popleft()

            embed = disnake.Embed(
                title="Now Playing",
                description=f"Now playing: '{song}'",
                color=disnake.Color.blurple()
            )
            await ctx.send(embed=embed)

            ydl_opts = {'format': 'bestaudio'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song, download=False)
                url2 = info['formats'][0]['url']

            self.voice.play(disnake.FFmpegPCMAudio(url2), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.bot.loop))

        else:
            await self.voice.disconnect()
            self.voice = None

def setup(bot):
    bot.add_cog(Music(bot))
