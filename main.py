import discord 
import yt_dlp
import asyncio
import os
import uuid
import shutil
from discord.ext import commands
from collections import deque

token = ""
intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents,case_insensitive=True)

music_queue = deque()
is_playing = False

os.makedirs("fila", exist_ok=True)


async def tocar(ctx:commands.Context): #toca a musica ou reproduz a tocar da fila
    global is_playing

    if music_queue:
        is_playing = True
        filepath, title = music_queue.popleft()
        source = discord.FFmpegPCMAudio(filepath)

        ctx_copy = ctx

        def after_play(error):
            if error:
                print(f"Erro ao tocar a música")
            
            try:
                os.remove(filepath) #apos a musica terminar e apagada da pasta fila

            except Exception as e:
                print(f"[ERRO ao apagar arquivo] {e}")

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

    filename = os.path.join("fila", f"{uuid.uuid4()}.webm") #salva a musica na pasta fila

    ydl_options = {'format': 'bestaudio[ext=webm]/bestaudio', 'outtmpl': filename, 'quiet': True} #escolher o melhor audio disponivel

    try: #baixa a musica
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download=True)['entries'][0]
            title = info['title']

    except Exception as e:
        await ctx.reply("Opa, ocorreu um erro ao buscar a música")
        print(f"[ERRO yt-dlp]{e}")
        return
    
    if is_playing:
        music_queue.append((filename, title))
        await ctx.send(f"Música {title} adicionada à fila")

    if not is_playing:
        music_queue.appendleft((filename, title))
        await tocar(ctx)

@bot.command(name="parar") #parar a musica
async def parar(ctx:commands.Context):
    global music_queue, is_playing
    voice = ctx.voice_client

    if voice and voice.is_playing():
        music_queue.clear()
        is_playing = False
        voice.stop()
        await voice.disconnect()

        await asyncio.sleep(1)

        try: #exclui a fila
            if os.path.exists("fila"):
                shutil.rmtree("fila")
                os.makedirs("fila", exist_ok=True)

        except Exception as e:
            print(f"[ERRO ao apagar a fila {e}]")

        await embed_stop(ctx)
    
    else: 
        await ctx.send("Opa, não estou tocando nenhuma música agora")

@bot.command(name="pausar") #pausar a musica
async def pausar(ctx:commands.Context):
    voice = ctx.voice_client
    if voice and voice.is_playing():
        voice.pause()
        await embed_pause(ctx)
    
    else:
        await ctx.send("Opa, não estou tocando nenhuma música no momento")

@bot.command(name="continuar") #continuar a musica
async def continuar(ctx:commands.Context):
    voice = ctx.voice_client
    if voice and voice.is_paused():
        voice.resume()
        await embed_resume(ctx)

    else:
        await ctx.send("Opa, nenhuma música está pausada")

#EMBEDS
async def embed_guide(ctx:commands.Context):
    embed_guide = discord.Embed(
    title="Guia de comandos do Orpheus:",
    description=".tocar nome da musica - toca a musica digitada ou coloca na fila\n.parar - interrompe as musicas e deleta a fila\n.pausar - pausa a música atual\n.continuar - continua a música pausada"
    )

    await ctx.send(embed=embed_guide)

async def embed_play(ctx:commands.Context, title: str):
    embed_play = discord.Embed(
    title="🎶 Tocando:",
    description=title,
    )
    embed_play.set_footer(text="Dica: digite '.parar' para interromper e '.pausar' para pausar, ou adicione uma musica na fila com '.tocar nome da musica'")

    await ctx.send(embed=embed_play)

async def embed_stop(ctx:commands.Context):
    embed_stop = discord.Embed(
        title="⏹ Música interrompida!"
    )

    await ctx.send(embed=embed_stop)

async def embed_pause(ctx:commands.Context):
    embed_pause = discord.Embed(
        title="⏸ Música pausada",
        description="Digite '.continuar' para voltar a ouvir"
    )

    await ctx.send(embed=embed_pause)

async def embed_resume(ctx:commands.Context):
    embed_resume = discord.Embed(
        title="▶ Música retomada"
    )

    await ctx.send(embed=embed_resume)

async def embed_apolo(ctx:commands.Context):
    embed_apolo = discord.Embed(
        title="Pedro, eu te amo como Jascinto amou apolo",
        description="assinado: Yan, seu amor"
    )

    await ctx.send(embed=embed_apolo)


#ONREADY
@bot.event 
async def on_ready():

    #reseta a pasta fila
    if os.path.exists("fila"):
        shutil.rmtree("fila")
        os.makedirs("fila", exist_ok=True)

    print("+++++ Orpheus está agora no ar! +++++")

bot.run(token)