import asyncio
import os

import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def setup():
    """Load commands (cog files) from the command file"""

    for cmd_file in os.listdir(settings.CMDS_DIR):
        if cmd_file.endswith(".py"):
            await bot.load_extension(f"commands.{cmd_file[:-3]}")


async def main():
    """The main function for setting up and running the bot"""

    async with bot:
        await setup()
        await bot.start(settings.BOT_SECRET)


if __name__ == "__main__":
    asyncio.run(main())
