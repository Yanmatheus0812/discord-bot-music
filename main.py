import discord 
import yt_dlp
import asyncio
from discord.ext import commands
from collections import deque

token = ""
intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents,case_insensitive=True)

music_queue = deque()
is_playing = False


async def tocar(ctx:commands.Context): #toca a musica ou reproduz a tocar da fila
    global is_playing

    if music_queue:
        is_playing = True
        url, title = music_queue.popleft()
        source = discord.FFmpegPCMAudio(url, options='-vn')

        ctx_copy = ctx

        def after_play(error):
            if error:
                print(f"Erro ao tocar a música")
            else:
                asyncio.run_coroutine_threadsafe(tocar(ctx_copy), bot.loop)

        try:
            ctx.voice_client.play(
                source, 
                after=after_play
            )
            await embed_play(ctx, title)

        except Exception as e:
            await ctx.send(f"Opa, me desculpe, nao consegui reproduzir {title}")
            print(f"[ERRO ffmpeg] {e}")
            await tocar(ctx)
    else:
        is_playing = False


# COMMANDS
@bot.command(name="apresentar") #apresentacao do Orpheus
async def apresentar(ctx:commands.Context):
    nome = ctx.author.name
    await ctx.send(f"Olá, {nome}! Sou o Orpheus, prazer em te conhecer! Sou um músico da grécia antiga e posso reproduzir músicas para você no discord, caso não saiba meus comandos pode digitar '.ajuda'!")

@bot.command(name="ajuda") #guia de comandos
async def ajuda(ctx:commands.Context):
    await embed_guide(ctx)

@bot.command(name="apolo")
async def apolo(ctx:commands.Context):
    await embed_apolo(ctx)

@bot.command(name="tocar") #busca a musica
async def buscar(ctx:commands.Context, *, search: str):
    if ctx.author.voice is None: #usuario nao esta em um canal de voz
        await ctx.send("Opa, você precisa estar em um canal de voz para eu tocar a música")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is None: #Orpheus entra no canal de voz
        await channel.connect()
    
    elif ctx.voice_client.channel != channel: #Orpheus troca de canal de voz
        await ctx.voice_client.move_to(channel)

    await ctx.send("Estou buscando sua música, aguarde um momento...")

    ydl_options = {'format': 'bestaudio'} #escolher o melhor audio disponivel

    try: #comeca a procurar a musica
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
            url = info['url']
            title = info['title']
    except Exception as e:
        await ctx.reply("Opa, ocorreu um erro ao buscar a música")
        print(f"[ERRO yt-dlp]{e}")
        return
    
    if is_playing:
        music_queue.append((url, title))
        await ctx.send(f"Música {title} adicionada à fila")

    if not is_playing:
        music_queue.appendleft((url, title))
        await tocar(ctx)

@bot.command(name="parar") #parar a musica
async def parar(ctx:commands.Context):
    global music_queue, is_playing
    voice = ctx.voice_client
    if voice and voice.is_playing():
        voice.stop()
        music_queue.clear()
        is_playing = False
        await embed_stop(ctx)
    
    else: 
        await ctx.send("Opa, não estou tocando nenhuma música agora")


#EMBEDS
async def embed_guide(ctx:commands.Context):
    embed_guide = discord.Embed(
    title="Guia de comandos do Orpheus:",
    description="'.tocar (nome da musica)' - toca a musica digitada\n'.parar' - interrompe as musicas e deleta a fila"
    )

    await ctx.send(embed=embed_guide)

async def embed_play(ctx:commands.Context, title: str):
    embed_play = discord.Embed(
    title="🎶 Tocando:",
    description=title,
    )
    embed_play.set_footer(text="Dica: digite '.parar' para interromper")

    await ctx.send(embed=embed_play)

async def embed_stop(ctx:commands.Context):
    embed_stop = discord.Embed(
        title="❌ Música interrompida!"
    )

    await ctx.send(embed=embed_stop)

async def embed_apolo(ctx:commands.Context):
    embed_apolo = discord.Embed(
        title="Pedro, eu te amo como Jascinto amou apolo",
        description="assinado: Yan, seu amor"
    )

    await ctx.send(embed=embed_apolo)


#ONREADY
@bot.event 
async def on_ready():
    print("+++++ Orpheus está agora no ar! +++++")

bot.run(token)