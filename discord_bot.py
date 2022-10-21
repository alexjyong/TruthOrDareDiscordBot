import discord
import os
import random
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        string_list= ["There is nothing wrong with pineapple on pizza", f'Hello there, {message.author.mention}!', "Tyler bullies Alex too much"]
        await message.channel.send(random.choice(string_list))
client.run(os.getenv('TOKEN'))
