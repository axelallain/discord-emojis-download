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
                with open(f"img{str(emoji.id)}.png", 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    if emoji.animated == True:
                        shutil.move(f"img{str(emoji.id)}.gif", f"stickers/img{str(emoji.id)}.gif")
                    else: 
                        shutil.move(f"img{str(emoji.id)}.png", f"stickers/img{str(emoji.id)}.png")
        shutil.make_archive('stickers', 'zip', 'stickers')

        for f in os.listdir('stickers'):
            os.remove(os.path.join('stickers', f))

        await message.channel.send(file=discord.File("stickers.zip"))

client.run(os.getenv("TOKEN"))
