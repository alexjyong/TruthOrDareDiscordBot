# Truth Or Dare Discord Bot

![TD2](https://user-images.githubusercontent.com/5464404/199782516-4c46c951-e5c2-43e0-ac6c-99ec05158462.png)

Truth or Dare Discord bot! Inspired by https://truthordarebot.xyz/. 

To run on your discord server, set up a bot with [guide](https://discordpy.readthedocs.io/en/stable/discord.html).

Clone this repo onto the server that you plan to run the bot out of. Within the repo, create a .env file.

With your favorite editor, add this to the file:
```
TOKEN='tokenFromTheLastStepHere'
BOTAUTHOR='WhatEverYouWantTheNameToBe'
```

(If you don't add in BOTAUTHOR, it will use the name `SysTD` by default.


install discord.py and python-dotenv via pip, then run
`python3 systd.py`

Or run via Docker with
`docker build -t discord-bot .`
then
`docker run -d -t discord-bot` 
