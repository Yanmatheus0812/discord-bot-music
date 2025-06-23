# Orpheus – Bot de Música para Discord

Orpheus é um bot de música feito em Python que busca, baixa e reproduz músicas do YouTube diretamente em canais de voz do Discord. Inspirado na mitologia grega, Orpheus representa a arte da música.  

Este foi um projeto criado como aprendizado pessoal e para uso entre amigos, não disponibilizado publicamente.

---

## Funcionalidades

- 🔍 Busca músicas no YouTube usando 
- 🎧 Reproduz o áudio localmente no canal de voz 
- ➕ Adiciona múltiplas músicas em uma fila
- ▶ Comandos de `pausar`, `continuar`, `parar` e `tocar`
- 🗂️ Baixa os arquivos temporários na pasta `fila/`
- 🧹 Limpeza automática dos arquivos após execução 

---

## Tecnologias e bibliotecas

- discord.py – integração com a API do Discord
- yt-dlp – para baixar o áudio do YouTube
- ffmpeg – usado para tocar o áudio (deve estar instalado no sistema)

---

## Comandos disponíveis

| Comando           | Descrição                                       |
|-------------------|-------------------------------------------------|
| `.tocar <música>` | Busca e toca a música ou adiciona à fila        |
| `.pausar`         | Pausa a música atual                            |
| `.continuar`      | Retoma a música pausada                         |
| `.parar`          | Interrompe tudo e limpa a fila                  |
| `.ajuda`          | Exibe os comandos disponíveis                   |
| `.apresentar`     | Orpheus se apresenta                            |


---

## Como rodar

### 1. Clone o repositório
```
git clone https://github.com/Yanmatheus0812/discord-bot-music/tree/main
```

### 2. Instale as dependências
```
pip install -r requirements.txt
```

### 3. Instale o FFmepeg
[Baixe o FFmpeg](https://www.gyan.dev/ffmpeg/builds/) e adicione ao PATH do sistema

### 4. Configure o token do bot
Crie um token para o seu bot através do site [discord developer portal](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiliaGHxYiOAxVrH7kGHVwCMp8QFnoECAkQAQ&url=https%3A%2F%2Fdiscord.com%2Fdevelopers%2Fapplications&usg=AOvVaw1wrZe_Tr9Sav0Zx4-42-Jf&opi=89978449)
Após isso, modifique o arquivo main.py na linha 10 em:
```
token = "SEU_TOKEN_AQUI"
```
Além disso, não esqueça de adicionar o bot ao seu servidor

### 5. Execute o bot
```
python main.py
```
