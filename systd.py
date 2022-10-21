import discord
import os
from dotenv import load_dotenv
load_dotenv()
from discord import app_commands
from discord.ui import Button, View
import random

def get_dare():
    dares = ["Change your discord server nickname to your high school nickname for 24 hours",
        "You have to leave an R-rated voicemail for an ex.",
        "show everyone your dick",
        "Give a detailed presentation on how you woo a lover in the style of a TED Talk.",
        "You have to say, “I’m just a silly boy,” and slap yourself gently on the face 20 times. Send the video.",
        "Scream. (Record it and send the audio.)",
        "Send the most unflattering picture of you that you have in your phone.",
        "Send the most recent text that you sent your mom.",
        "Post a picture of your feet",
        "Drink a full bottle of water"
    ]
    dare = random.choice(dares)
    return dare

def get_truth():
    truths = ["What is the song that you get it on to the most?",
        "How many people have you slept with?",
        "Who here are you most jealous of?",
        "When was the last time you cried?",
        "What are you wearing?",
        "If I went through your room, what would I be surprised to find?",
        "Are you turned on right now?",
        "how hard would you spank me?",
        "Do you remember the first time you came? What were you thinking when it happened?",
        "What is your most bizarre sex story?",
        "What street did you grow up on? What is the name of your childhood pet? Who was your first grade teacher? What is your mother's maiden name?",
        "When is the last time you lied about feeding your dog?",
        "How much have you spent on OF?",
        "How much would you spend on sysengineer's OF?",
    ]
    truth = random.choice(truths)
    return truth

def gen_embed(person,color_code,choice):
    embed=discord.Embed(title=person, color=color_code)
    embed.set_author(name="SysTD")
    if choice == "Dare":
        td_value = get_dare()
    elif choice == "Truth":
        td_value = get_truth()
    else:
        td_value = "ERROR"
    embed.add_field(name=f"Your {choice}:", value=td_value, inline=False)
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
    """Get a SysTD"""
    color_code = 0x0000ff
    embed=discord.Embed(title=interaction.user.display_name, color=color_code)
    embed.set_author(name="SysTD")
    
    async def button_truth_callback(interaction):
        color_code = 0x0000ff
        choice = "Truth"
        person = interaction.user.display_name
        embed = gen_embed(person, color_code, choice)
        await interaction.response.send_message(embed=embed, view=view)
        return None
    
    async def button_dare_callback(interaction):
        color_code = 0xff0000
        choice = "Dare"
        person = interaction.user.display_name
        embed = gen_embed(person, color_code, choice)
        await interaction.response.send_message(embed=embed, view=view)
        return None
    
    button_truth = Button(label="Truth", style=discord.ButtonStyle.primary)
    button_dare = Button(label="Dare", style=discord.ButtonStyle.danger)
    button_truth.callback = button_truth_callback
    button_dare.callback = button_dare_callback
    view = View()
    view.add_item(button_truth)
    view.add_item(button_dare)
    await interaction.response.send_message(embed=embed, view=view)
    return None

client.run(os.getenv('TOKEN'))