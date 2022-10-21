import discord
import os
import random

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
client.run('<REDACTED>')#this should be in an env file, but i'm a terrible person and haven't set that up yet.
