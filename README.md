# JackO'Lantern
This is a discord music bot, written in python. It uses **yt-dlp** to stream music from youtube. This project if meant for people who are starting development with python, discord.py, ytdl and discord API, because I know how I felt when I was at the begining and I hope that this application will clear some issues that I faced at some point and had a hard time figuring them out. More documentation will be added in the future. Enjoy!

### Directory hierarchy

- JACKO_LANTERN
	- commands
		- developer.py
		- music.py
		- utility.py
	- utils
		- music_player.py
		- music_utils.py
		- ytdl_utils.py
	- bot.py (main file)
	- settings.py

### Dependencies
- yt-dlp
- discord
- asyncio
- python 3.10 and above

### Getting started
Before you run the main file into an IDE or console, there are a couple of things to do.
Firstly, you need to generate your bot TOKEN, from the [Discord Developer Portal](https://discord.com/developers) site. After that, you need to copy it and put it inside a **.env** file, placed on the same level as the bot.py file (in the JackoLantern directory, if you just cloned the repository on your system) and name the variable TOKEN (this can be changed from the settings.py file).

Secondly and lastly, you need to create a folder named logs placed on the same level as bot.py (here your log files will be placed).

After all this, you are free to invite your bot on the server and start it up.

### Commands
Here are all the commands available at this moment:

- play
- stop
- resume
- pause
- queue
- now playing
- remove
- join
- leave
- load
- reload
- unload

For more information, use the !help command in the discord chat.

### Troubleshooting and development
For easier troubleshooting and your own development ideas, you have the right, as administrator, to run one of 3 commands: **load**, **unload** and **reload**. These are for loading, unloading and reloading cogs while the bot is running so you don't have to stop it and start it manually. The syntax is **! < command >< cog >**, where **cog** is the exact name of the **.py** file you are trying to modify (the cog file).

### Version
Version 1.0
