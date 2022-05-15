#!/usr/bin/env python3

import discord
from discord.ext import commands
import requests
import shutil
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=".", intents=intents)

@client.event
async def on_message(message):
    if message.content.startswith('>>getstickers'):
        for emoji in message.guild.emojis:
            url = "https://cdn.discordapp.com/emojis/" + str(emoji.id)
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                for i in range(len(message.guild.emojis)):
                    with open(f"img{str(i)}.png", 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                        shutil.move(f"img{str(i)}.png", f"stickers/img{str(i)}.png")
        shutil.make_archive('stickers', 'zip', 'stickers')
        await message.channel.send(file=discord.File("stickers.zip"))

client.run(os.getenv("TOKEN"))