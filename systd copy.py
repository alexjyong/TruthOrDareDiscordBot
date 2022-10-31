import discord
import os
from dotenv import load_dotenv

load_dotenv()
from discord import app_commands
from discord.ui import Button, View
import random
import csv

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
    global sent_msg, embed
    color_code = 0x0000FF
    embed = discord.Embed(title=interaction.user.display_name, color=color_code)
    embed.set_author(name=bot_author)
    embed.set_thumbnail(url='https://sharepointlist.com/images/TD2.png')

    class MyButton(Button):
        '''This is not being used yet because I'm not sure what's wrong with it'''
        async def callback(self, interaction: interaction):
            if self.label == "Truth" or self.label == "NSFW Truth":
                color_code = 0x0000FF
                type = "Truth"
            elif self.label == "Dare" or self.label == "NSFW Dare":
                color_code = 0xFF0000
                type = "Dare"
            if self.label == "NSFW Truth" or self.label == "NSFW Dare":
                nsfw = "Yes"
            else:
                nsfw = "No"
            person = interaction.user.display_name
            embed = gen_embed(person, color_code, type, nsfw=nsfw)
            await interaction.response.send_message(embed=embed, view=view)




    async def button_callback(interaction: interaction, type, nsfw):
        global sent_msg, embed
        await sent_msg.edit(embed=embed, view=None)
        if type == "Truth":
            color_code = 0x0000FF
        if type == "Dare":
            color_code = 0xFF0000
        person = interaction.user.display_name
        if nsfw == "Yes":
            embed = gen_embed(person, color_code, type, nsfw="Yes")
        else:
            embed = gen_embed(person, color_code, type)
        await interaction.response.send_message(embed=embed, view=view)
        sent_msg = await interaction.original_response()
        return None

    async def button_truth_callback(interaction):
        global sent_msg, embed
        await sent_msg.edit(embed=embed, view=None)
        color_code = 0x0000FF
        type = "Truth"
        person = interaction.user.display_name
        embed = gen_embed(person, color_code, type)
        await interaction.response.send_message(embed=embed, view=view)
        sent_msg = await interaction.original_response()
        return None

    async def button_dare_callback(interaction):
        global sent_msg, embed
        await sent_msg.edit(embed=embed, view=None)
        color_code = 0xFF0000
        type = "Dare"
        person = interaction.user.display_name
        embed = gen_embed(person, color_code, type)
        await interaction.response.send_message(embed=embed, view=view)
        sent_msg = await interaction.original_response()
        return None

    async def button_truth_nsfw_callback(interaction):
        global sent_msg, embed
        await sent_msg.edit(embed=embed, view=None)
        color_code = 0x0000FF
        type = "Truth"
        person = interaction.user.display_name
        embed = gen_embed(person, color_code, type, nsfw="Yes")
        await interaction.response.send_message(embed=embed, view=view)
        sent_msg = await interaction.original_response()
        return None

    async def button_dare_nsfw_callback(interaction):
        global sent_msg, embed
        await sent_msg.edit(embed=embed, view=None)
        color_code = 0xFF0000
        type = "Dare"
        person = interaction.user.display_name
        embed = gen_embed(person, color_code, type, nsfw="Yes")
        await interaction.response.send_message(embed=embed, view=view)
        sent_msg = await interaction.original_response()
        return None

    button_truth = Button(label="Truth", style=discord.ButtonStyle.primary)
    button_dare = Button(label="Dare", style=discord.ButtonStyle.danger)
    button_truth_nsfw = Button(label="NSFW Truth", style=discord.ButtonStyle.primary)
    button_dare_nsfw = Button(label="NSFW Dare", style=discord.ButtonStyle.danger)
    button_truth.callback = button_truth_callback
    button_dare.callback = button_dare_callback
    button_truth_nsfw.callback = button_truth_nsfw_callback
    button_dare_nsfw.callback = button_dare_nsfw_callback
    # button_truth.callback = button_callback(interaction, type="Truth", nsfw="No")
    # button_dare.callback = button_callback(interaction, type="Dare", nsfw="No")
    # button_truth_nsfw.callback = button_callback(interaction, type="Truth", nsfw="Yes")
    # button_dare_nsfw.callback = button_callback(interaction, type="Dare", nsfw="Yes")

    view = View()
    view.add_item(button_truth)
    view.add_item(button_dare)
    view.add_item(button_truth_nsfw)
    view.add_item(button_dare_nsfw)

    # ***** This is what I'm working toward with a single function *****
    # view = View(...)
    # labels = ("Truth", "Dare", "NSFW Truth", "NSFW Dare")
    # vw = View(...)
    # for label in labels:
    #     vw.add_item(MyButton(label=label))


    await interaction.response.send_message(embed=embed, view=view)
    sent_msg = await interaction.original_response()
    return None


client.run(os.getenv("TOKEN"))
