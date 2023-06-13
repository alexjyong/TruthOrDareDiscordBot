import discord
import os
import sqlite3
import random
import asyncio
from discord import app_commands
from discord.ui import Button, View
from dotenv import load_dotenv

load_dotenv()

truths_pg = []
truths_nsfw = []
dares_pg = []
dares_nsfw = []


def gen_tds():
    """Generate four lists for the Truth or Dares"""
    conn = sqlite3.connect('tds.db')
    c = conn.cursor()

    for row in c.execute('SELECT * FROM tds'):
        td = row[5]
        type = row[6]
        value = row[7]
        if td == "Truth":
            if type == "SFW":
                truths_pg.append(value)
            elif type == "NSFW":
                truths_nsfw.append(value)
        elif td == "Dare":
            if type == "SFW":
                dares_pg.append(value)
            elif type == "NSFW":
                dares_nsfw.append(value)

    conn.close()


gen_tds()

truths_pg_master = truths_pg.copy()
truths_nsfw_master = truths_nsfw.copy()
dares_pg_master = dares_pg.copy()
dares_nsfw_master = dares_nsfw.copy()

bot_author = os.getenv("BOTAUTHOR")
print(bot_author)
if bot_author == None:
    bot_author = "SysTD"

def gen_embed(person, color_code, type, nsfw="No"):
    global dares_nsfw, dares_nsfw_master, dares_pg, dares_pg_master, truths_nsfw, truths_nsfw_master, truths_pg, truths_pg_master
    embed = discord.Embed(title=person, color=color_code)
    embed.set_author(name=bot_author)
    if type == "Dare" and nsfw == "Yes":
        from_list = dares_nsfw
    elif type == "Dare" and nsfw == "No":
        from_list = dares_pg
    elif type == "Truth" and nsfw == "Yes":
        from_list = truths_nsfw
    elif type == "Truth" and nsfw == "No":
        from_list = truths_pg
    else:
        from_list = truths_pg
    td_value = random.choice(from_list)
    from_list.remove(td_value)
    if len(dares_nsfw) < 1:
        dares_nsfw = dares_nsfw_master.copy()
    if len(dares_pg) < 1:
        dares_pg = dares_pg_master.copy()
    if len(truths_nsfw) < 1:
        truths_nsfw = truths_nsfw_master.copy()
    if len(truths_pg) < 1:
        truths_pg = truths_pg_master.copy()
    type_name = ""
    if nsfw == "Yes":
        type_name = "NSFW "
    type_name += type
    embed.add_field(name=f"Your {type_name}:", value=td_value, inline=False)
    embed.set_thumbnail(url='https://sharepointlist.com/images/TD2.png')
    return embed

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    guild_count = 0
    for guild in client.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1
    print(f"Bot is in {guild_count} guilds.")
    print("Bot Ready!")

class NSFWOption(app_commands.Option):
    async def callback(self, ctx, value):
        ctx.data["nsfw"] = value

class DareButton(Button):
    async def callback(self, interaction: discord.Interaction):
        color_code = discord.Color.red()
        person = interaction.user.name
        nsfw = interaction.message.interaction.data["nsfw"]
        embed = gen_embed(person, color_code, "Dare", nsfw)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class TruthButton(Button):
    async def callback(self, interaction: discord.Interaction):
        color_code = discord.Color.blue()
        person = interaction.user.name
        nsfw = interaction.message.interaction.data["nsfw"]
        embed = gen_embed(person, color_code, "Truth", nsfw)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class TruthOrDareView(View):
    def __init__(self):
        super().__init__()
        self.add_item(TruthButton(style=Button.style.green, label='Truth'))
        self.add_item(DareButton(style=Button.style.red, label='Dare'))

@client.tree.command()
async def truthordare(ctx, nsfw: NSFWOption("NSFW?", app_commands.OptionType.boolean, default=False)):
    await ctx.send("Please select Truth or Dare!", view=TruthOrDareView(), ephemeral=True)

client.run(os.getenv("DISCORD_TOKEN"))
