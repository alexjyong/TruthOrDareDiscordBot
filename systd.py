import discord
import os
from dotenv import load_dotenv

load_dotenv()
from discord import app_commands
from discord.ui import Button, View
import random
import csv
import asyncio

truths_pg = []  ## Initialize
truths_nsfw = []  ## Initialize
dares_pg = []  ## Initialize
dares_nsfw = []  ## Initialize

def gen_tds():
    """Generate four lists for the Truth or Dares"""
    with open("tds.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            td = row["What is it?"]
            type = row["Type"]
            value = row["Truth or Dare"]
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


gen_tds()  ## Run it once on load
# copy all to master lists
truths_pg_master = truths_pg.copy()
truths_nsfw_master = truths_nsfw.copy()
dares_pg_master = dares_pg.copy()
dares_nsfw_master = dares_nsfw.copy()

bot_author = os.getenv("BOTAUTHOR")
print(bot_author)
if bot_author == None: #use this as default name if the user didn't set it.
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
    else:  ## Change this later.
        from_list = truths_pg
    td_value = random.choice(from_list)
    from_list.remove(td_value)
    # If any list got emptied, copy it from the master
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
    '''Start the truth or dare activity'''
    global sent_msg, embed, sleep_time, sleep_task
    sleep_time = 300
    color_code = 0x0000FF
    embed = discord.Embed(title=interaction.user.display_name, color=color_code)
    embed.set_author(name=bot_author)
    embed.set_thumbnail(url='https://sharepointlist.com/images/TD2.png')

    async def sleep_timer():
        global sleep_task
        try:
            print("Starting sleep timer")
            await asyncio.sleep(sleep_time)
        except asyncio.CancelledError: # if it was canceled
            # probably don't need the except since I'm not actually doing anything with it
            print("Sleep timer canceled")
            raise
        else: # if it wasn't canceled
            print("Sleep timer expired. Refreshing bot message and removing buttons")
            embed.add_field(name="Status", value="The current game has timed out. Send /play to start again")
            await sent_msg.edit(embed=embed, view=None)
            # Send a new message
            #sleep_task = asyncio.create_task(sleep_timer())
        #finally: # Don't need a finally atm either
            
    class MyButton(Button):
        async def callback(self, interaction: interaction):
            global sent_msg, embed, style, sleep_task
            # Cancel refresh timer
            sleep_task.cancel()
            await sent_msg.edit(embed=embed, view=None)
            if self.label == "Truth" or self.label == "NSFW Truth":
                color_code = 0x0000FF
                type = "Truth"
                self.style=discord.ButtonStyle.primary
            elif self.label == "Dare" or self.label == "NSFW Dare":
                color_code = 0xFF0000
                type = "Dare"
                self.style=discord.ButtonStyle.danger
            if self.label == "NSFW Truth" or self.label == "NSFW Dare":
                nsfw = "Yes"
            else:
                nsfw = "No"
            person = interaction.user.display_name
            embed = gen_embed(person, color_code, type, nsfw=nsfw)
            await interaction.response.send_message(embed=embed, view=view)
            sent_msg = await interaction.original_response()
            # Restart refresh timer
            sleep_task = asyncio.create_task(sleep_timer())

    view = View(timeout=330)
    labels = ("Truth", "Dare", "NSFW Truth", "NSFW Dare")
    for label in labels:
        if label == "Truth" or label == "NSFW Truth":
            style = discord.ButtonStyle.primary
        else:
            style = discord.ButtonStyle.danger
        view.add_item(MyButton(label=label, style=style))

    await interaction.response.send_message(embed=embed, view=view)
    sent_msg = await interaction.original_response()
    sleep_task = asyncio.create_task(sleep_timer())

@client.tree.command()
@app_commands.describe(truth_or_dare="Truth or Dare?")
@app_commands.choices(truth_or_dare=[
    app_commands.Choice(name="Truth", value="Truth"),
    app_commands.Choice(name="Dare", value="Dare")
])
@app_commands.describe(nsfw_or_nah="Is it NSFW or PG?")
@app_commands.choices(nsfw_or_nah=[
    app_commands.Choice(name="NSFW", value="Yes"),
    app_commands.Choice(name="PG", value="No")
])
@app_commands.rename(tdinput='content')
@app_commands.describe(tdinput='Your Truth or Dare')
async def addtd(interaction: discord.Interaction, truth_or_dare: app_commands.Choice[str], nsfw_or_nah: app_commands.Choice[str], tdinput: str):
    """Add a new item to the Truth or Dare bot"""
    print("test")
    print(f"{truth_or_dare.value} {nsfw_or_nah.value} {tdinput}")
    if (nsfw_or_nah.value == "Yes"):
        nsfw = "Yes"
        rating = "NSFW"
    else:
        nsfw = "No"
        rating = "PG"
    await interaction.response.send_message(f"You are trying to enter \"{tdinput}\" as a {rating} {truth_or_dare.value}\nThe bot is not processing submissions at this time")

@client.tree.command()
# @has_permissions(administrator=True)
async def setchan(interaction: discord.Interaction):
    '''Set the channel for the bot for this server'''
    global sent_msg, embed
    channel =  interaction.channel
    server = interaction.guild
    sender = interaction.user
    #await sent_msg.edit(embed=embed, view=None)
    if sender.guild_permissions.administrator:
        global sent_msg
        class MyButton(Button):
            async def callback(self, interaction: interaction):
                global sent_msg, embed, style, sleep_task
                if self.label == "Yes":
                    self.style=discord.ButtonStyle.primary
                    title = "You clicked yes. This is the part where I'd write that into the database"
                else:
                    title = "Please run this command in the channel that you want to set for the bot"
                    self.style=discord.ButtonStyle.danger
                embed = discord.Embed(title=title)
                embed.set_author(name=bot_author)
                await sent_msg.edit(embed=embed, view=None)
                #await interaction.response.send_message(embed=embed) # removed the view here; don't want the buttons at this point
        

        view = View()
        labels = ("Yes", "No")
        for label in labels:
            if label == "Yes":
                style = discord.ButtonStyle.primary
            else:
                style = discord.ButtonStyle.danger
            view.add_item(MyButton(label=label, style=style))
        title = f"Do you want to set this channel ({channel.name}) for the {bot_author} bot?"
        embed = discord.Embed(title=title)
        embed.set_author(name=bot_author)
        await interaction.response.send_message(embed=embed, view=view)
        sent_msg = await interaction.original_response()        
        #await interaction.response.send_message(f"You are in channel {channel} with id: {channel.id}\nOn server: {server.name} with id: {server.id}\n{sender}")
    else:
        await interaction.response.send_message(f"You do not have the necessary permissions to perform this command")



client.run(os.getenv("TOKEN"))
