import asyncio
import discord
from discord.ext import commands
from pytube import YouTube

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("Entra na sala primeiro ")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command()
async def play(ctx, url):
    server = ctx.message.guild
    voice_channel = server.voice_client
    try:
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('**Tocando:** {}'.format(player.title))
    except Exception as e:
        print(e)
        await ctx.send('Ih, Deu ruim.')


@bot.command()
async def leave(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    await voice_channel.disconnect()

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        file = video.download()
        return cls(discord.FFmpegPCMAudio(file), data={'title': yt.title, 'url': url})
    

bot.run('SEU TOKEN')
