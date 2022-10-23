import discord
import os
from dotenv import load_dotenv
load_dotenv()
from discord import app_commands
from discord.ui import Button, View
import random
import csv

def get_td(type,nsfw="No"):
    tds = []
    with open('tds.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["What is it?"] == type and row["NSFW?"] == nsfw:
                tds.append(row["Truth or Dare"])
        td = random.choice(tds)
    print(td)
    return td


def gen_embed(person,color_code,type,nsfw="No"):
    embed=discord.Embed(title=person, color=color_code)
    embed.set_author(name="SysTD")
    td_value = get_td(type, nsfw)
    #td_value = "ERROR"
    type_name = ""
    if nsfw == "Yes":
        type_name = "NSFW "
    type_name += type
    embed.add_field(name=f"Your {type_name}:", value=td_value, inline=False)
    return embed

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        await self.tree.sync()

intents = discord.Intents.default()
client = MyClient(intents=intents)

# Event Listener when going online
@client.event
async def on_ready():
	# Counter to track how many servers bot is connected to
	guild_count = 0
	# Loop through servers
	for guild in client.guilds:
		# Print server name and ID
		print(f"- {guild.id} (name: {guild.name})")
		guild_count = guild_count + 1
	# Print total
	print("SysTD is in " + str(guild_count) + " servers.")

@client.tree.command()
async def play(interaction: discord.Interaction):
    color_code = 0x0000ff
    embed=discord.Embed(title=interaction.user.display_name, color=color_code)
    embed.set_author(name="SysTD")
    
    async def button_truth_callback(interaction):
        color_code = 0x0000ff
        type = "Truth"
        person = interaction.user.display_name
        embed = gen_embed(person, color_code, type)
        await interaction.response.send_message(embed=embed, view=view)
        return None
    
    async def button_dare_callback(interaction):
        color_code = 0xff0000
        type = "Dare"
        person = interaction.user.display_name
        embed = gen_embed(person, color_code, type)
        await interaction.response.send_message(embed=embed, view=view)
        return None

    async def button_truth_nsfw_callback(interaction):
        color_code = 0x0000ff
        type = "Truth"
        person = interaction.user.display_name
        embed = gen_embed(person, color_code, type, nsfw="Yes")
        await interaction.response.send_message(embed=embed, view=view)
        return None
    
    async def button_dare_nsfw_callback(interaction):
        color_code = 0xff0000
        type = "Dare"
        person = interaction.user.display_name
        embed = gen_embed(person, color_code, type, nsfw="Yes")
        await interaction.response.send_message(embed=embed, view=view)
        return None
    
    button_truth = Button(label="Truth", style=discord.ButtonStyle.primary)
    button_dare = Button(label="Dare", style=discord.ButtonStyle.danger)
    button_truth_nsfw = Button(label="NSFW Truth", style=discord.ButtonStyle.primary)
    button_dare_nsfw = Button(label="NSFW Dare", style=discord.ButtonStyle.danger)
    button_truth.callback = button_truth_callback
    button_dare.callback = button_dare_callback
    button_truth_nsfw.callback = button_truth_nsfw_callback
    button_dare_nsfw.callback = button_dare_nsfw_callback
    view = View()
    view.add_item(button_truth)
    view.add_item(button_dare)
    view.add_item(button_truth_nsfw)
    view.add_item(button_dare_nsfw)
    await interaction.response.send_message(embed=embed, view=view)
    return None

client.run(os.getenv('TOKEN'))