import settings

import random

import discord
from discord.ext import commands

status_list = ["Eminem", "Adele", "Queen", "The Beatles", "Pending..."]
logger = settings.logging.getLogger("bot")


class Utility(commands.Cog):
    """
    A utility cog for various bot functions.

    This cog provides utility functions for the bot, including:

    - Setting the bot's status and activity when it's ready.
    - Allowing the bot to join the voice channel where the user is.
    - Allowing the bot to leave the voice channel it's currently in.

    Attributes:

    -  bot :  :class:`discord.ext.commands.Bot`: The bot instance associated with this cog.

    Functions:

    - on_ready: A listener method that sets the bot's status and logs that it is online.
    - join: A command to make the bot join the voice channel of the invoking user.
    - leave: A command to make the bot leave the voice channel it's in.
    """

    def __init__(self, bot):
        """
        Initializes the Utility cog.

        Args:
            bot :  :class:`discord.ext.commands.Bot`: The bot instance to associate with this cog.

        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        A listener method that sets the bot's status and logs that it is online.
        """

        status = status_list[random.randint(0, len(status_list) - 1)]
        await self.bot.change_presence(status=discord.Status.idle,
                                       activity=discord.Activity(type=discord.ActivityType.listening,
                                                                 name=status))
        logger.info(str(self.bot.user).split("#")[0] + " is online")

    @commands.command(help="Makes the bot join the voice channel you are in")
    async def join(self, ctx: discord.ext.commands.Context):
        """
        A command to make the bot join the voice channel of the invoking user.

        Args:
            ctx:    :class:`discord.ext.commands.Context`: The context of the command invocation.

        """

        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client:
                await ctx.voice_client.disconnect()
                await channel.connect()
            else:
                await channel.connect()
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command!")

    @commands.command(help="Makes the bot leave the voice channel you are in")
    async def leave(self, ctx: discord.ext.commands.Context):
        """
        A command to make the bot leave the voice channel it's in.

        Args:
            ctx:    :class:`discord.ext.commands.Context`: The context of the command invocation.

        """

        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("I left the voice channel")
        else:
            await ctx.send("I am not in a voice channel")


async def setup(bot):
    await bot.add_cog(Utility(bot))
