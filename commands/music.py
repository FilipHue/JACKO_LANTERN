import math
from datetime import datetime

import discord
from discord.ext import commands

from utils import music_utils
from utils import music_player
from utils import ytdl_utils

player_handler = music_player.PlayerHandler()


class Music(commands.Cog):
    """
    A music cog for controlling bot's audio playback in voice channels.

    This cog provides commands to control audio playback such as: playing, pausing, resuming,
    stopping, and managing the queue.

    Attributes:
        bot:    :class:`commands.Bot`: The bot instance associated with this cog.

        find_url:   :class:`function` --> A function to find a valid URL from a song name.

    """

    def __init__(self, bot: commands.Bot):
        """
        Initializes the Music cog.

        Args:
            bot (commands.Bot): The bot instance associated with this cog.

        """
        self.bot = bot
        self.find_url = music_utils.find_url

    @commands.command(aliases=["p"], help="Queues and plays a song")
    async def play(self, ctx: discord.ext.commands.Context, *, names):
        """
        Queues and plays a song or songs in the voice channel.

        Args:
            ctx:    :class:`discord.ext.commands.Context`: The context of the command invocation.
            names:  :class:`str`: A comma-separated list of song names or keywords to search for or urls.

        """

        embed_message = discord.Embed()

        for name in names.split(","):
            url = self.find_url(name)

            player = player_handler.get_player(ctx)
            if player is None:
                player = player_handler.create_player(ctx, ffmpeg_options=ytdl_utils.ffmpeg_options)

            if not ctx.voice_client.is_playing():
                await player.queue(url)
                song = await player.play()

                embed_message.set_author(name=f"Let the Music Play!")
                embed_message.set_thumbnail(url=song.thumbnail)

                embed_message.add_field(name=f"🎵 Now spinning:",
                                        value=f"[{song.title}]({song.url})")
                embed_message.add_field(name=":microphone: By:",
                                        value=f"[{song.channel}]({song.channel_url})", inline=True)
                embed_message.add_field(name=f":timer: Duration: {song.duration}",
                                        value=f"", inline=False)

                embed_message.add_field(name=":mega: Get ready to groove! The music is back and better than ever.",
                                        value="", inline=False)

                embed_message.colour = discord.Colour.dark_blue()
                await ctx.send(embed=embed_message)
            else:
                song = await player.queue(url)
                embed_message.set_author(name=f'Song added to queue!')
                embed_message.set_thumbnail(url=song.thumbnail)

                embed_message.add_field(name=f"🎵 Latest addition:",
                                        value=f"[{song.title}]({song.url})", inline=True)
                embed_message.add_field(name=":microphone: By:",
                                        value=f"[{song.channel}]({song.channel_url})", inline=True)
                embed_message.add_field(name=f":timer: Duration: {song.duration}",
                                        value=f"", inline=False)
                embed_message.add_field(name=f":card_index: Position in"
                                             f"queue: {len(player.handler.queue[ctx.guild]) - 1}",
                                        value=f"", inline=True)

                embed_message.add_field(name=f":loud_sound: Exciting choices ahead! Feel free to explore the queue or "
                                             f"use playback commands to enjoy the music.",
                                        value="", inline=False)

                embed_message.colour = discord.Colour.dark_blue()
                await ctx.send(embed=embed_message)

    @commands.command(help="Stops the playlist and clears the queue")
    async def stop(self, ctx: discord.ext.commands.Context):
        """
        Stops the current playlist and clears the queue.

        Args:
            ctx:    :class:`discord.ext.commands.Context`: The context of the command invocation.

        """

        player = player_handler.get_player(ctx)
        embed_message = discord.Embed()

        if player and player.voice.is_playing():
            await player.stop()

            embed_message.set_author(name="Music playback has been stopped!")

            embed_message.add_field(name=":octagonal_sign: The music has stopped and the queue has been cleared!",
                                    value="", inline=False)
            embed_message.add_field(name=":cricket: Enjoy the silence, for now.",
                                    value="", inline=False)
            embed_message.add_field(name="What's next?",
                                    value="", inline=False)
            embed_message.add_field(name="",
                                    value=f"- Want to play another song?"
                                          f"Use the play command to continue.", inline=False)
            embed_message.add_field(name="",
                                    value=f"- Looking for more commands?"
                                          f"Type !help to explore all the available options.", inline=False)

            embed_message.colour = discord.Colour.dark_purple()
        elif player and not player.voice.is_playing():
            embed_message.set_author(name="No Music is Playing")

            embed_message.add_field(name=f"🎵 There's currently no music playing to stop. Enjoy the calm!",
                                    value="", inline=False)
            embed_message.add_field(name="What can you do?",
                                    value="", inline=False)
            embed_message.add_field(name="",
                                    value=f"- Want to start a music session?"
                                          f"Use the play command to get the party started!",
                                    inline=False)
            embed_message.add_field(name="",
                                    value=f"- Looking for more commands?"
                                          f"Type !help to explore all the available options.",
                                    inline=False)

            embed_message.colour = discord.Colour.dark_purple()
        else:
            embed_message.set_author(name="No Voice Connection")

            embed_message.add_field(name=f"🔇 There's no active voice connection to stop."
                                         f"You're already enjoying the silence.",
                                    value="", inline=False)
            embed_message.add_field(name="What can you do?",
                                    value="", inline=False)
            embed_message.add_field(name="",
                                    value=f"- Want to start a music session?"
                                          f"Use the play command to get the party started!",
                                    inline=False)
            embed_message.add_field(name="",
                                    value=f"- Looking for more commands?"
                                          f"Type !help to explore all the available options.",
                                    inline=False)

            embed_message.colour = discord.Colour.dark_red()

        await ctx.send(embed=embed_message)

    @commands.command(help="Resumes the song")
    async def resume(self, ctx: discord.ext.commands.Context):
        """
        Resumes playback of the paused song.

        Args:
            ctx:    :class:`discord.ext.commands.Context`: The context of the command invocation.

        """

        player = player_handler.get_player(ctx)
        embed_message = discord.Embed()

        if player and not player.voice.is_playing():
            await player.resume()

            embed_message.set_author(name="Music Playback Resumed!")

            song = player.handler.queue[ctx.guild][0].song
            embed_message.add_field(name=f"⏯️ The music is back on track!",
                                    value=f"[{song.title}]({song.url}) by "
                                          f"[{song.channel}]({song.channel_url}) continues to play.",
                                    inline=False)
            embed_message.add_field(name=f"🎧 Now is the time to relax and enjoy the rhythms.",
                                    value="", inline=False)

            embed_message.colour = discord.Colour.dark_blue()
        elif player and player.voice.is_playing():
            embed_message.set_author(name="Keep the Party Rolling!")

            song = player.handler.queue[ctx.guild][0].song
            embed_message.add_field(name="",
                                    value=f"🎵 [{song.title}]({song.url}) by "
                                         f"[{song.channel}]({song.channel_url}) is already setting the mood!",
                                    inline=False)
            embed_message.add_field(name=f"🎧 The music never stops on Discord. Let's keep the party going!",
                                    value="", inline=False)

            embed_message.colour = discord.Colour.dark_blue()
        else:
            embed_message.set_author(name="No Voice Connection")

            embed_message.add_field(name=f"🔇 There's no active voice connection to resume.",
                                    value="", inline=False)
            embed_message.add_field(name="What can you do?",
                                    value="", inline=False)
            embed_message.add_field(name="",
                                    value=f"- Want to start a music session?"
                                          f"Use the play command to get the party started!",
                                    inline=False)
            embed_message.add_field(name="",
                                    value=f"- Looking for more commands?"
                                          f"Type !help to explore all the available options.",
                                    inline=False)

            embed_message.colour = discord.Colour.dark_red()

        await ctx.send(embed=embed_message)

    @commands.command(help="Pauses the song")
    async def pause(self, ctx: discord.ext.commands.Context):
        """
       Pauses the currently playing song.

       Args:
            ctx:    :class:`discord.ext.commands.Context`: The context of the command invocation.

       """

        player = player_handler.get_player(ctx)
        embed_message = discord.Embed()

        if player and player.voice.is_playing():
            await player.pause()

            embed_message.set_author(name="Music Paused!")

            song = player.handler.queue[ctx.guild][0].song
            embed_message.add_field(name="",
                                    value=f"⏸️ [{song.title}]({song.url}) by "
                                          f"[{song.channel}]({song.channel_url}) is taking a short break.",
                                    inline=False)
            embed_message.add_field(name=f"⏯️ Ready to continue the groove? Use the resume command when you're ready!",
                                    value="", inline=False)

            embed_message.colour = discord.Colour.dark_blue()
        elif player and not player.voice.is_playing():
            embed_message.set_author(name="No Music Playing")

            embed_message.add_field(name="🎵 There's currently no music playing to pause. Silence is golden!",
                                    value="",
                                    inline=False)
            embed_message.add_field(name="What can you do?",
                                    value="", inline=False)
            embed_message.add_field(name="",
                                    value=f"- Want to start a music session?"
                                          f"Use the play command to get the party started!",
                                    inline=False)
            embed_message.add_field(name="",
                                    value=f"- Looking for more commands?"
                                          f"Type !help to explore all the available options.",
                                    inline=False)

            embed_message.colour = discord.Colour.dark_blue()
        else:
            embed_message.set_author(name="No Voice Connection")

            embed_message.add_field(name=f"🔇 There's no active voice connection to pause.",
                                    value="", inline=False)
            embed_message.add_field(name="What can you do?",
                                    value="", inline=False)
            embed_message.add_field(name="",
                                    value=f"- Want to start a music session?"
                                          f"Use the play command to get the party started!",
                                    inline=False)
            embed_message.add_field(name="",
                                    value=f"- Looking for more commands?"
                                          f"Type !help to explore all the available options.",
                                    inline=False)

            embed_message.colour = discord.Colour.dark_red()

        await ctx.send(embed=embed_message)

    @commands.command(aliases=["q"], help="Shows the queue")
    async def queue(self, ctx: discord.ext.commands.Context):
        """
        Displays the current song queue.

        Args:
            ctx:    :class:`discord.ext.commands.Context`: The context of the command invocation.

        """
        player = player_handler.get_player(ctx)
        embed_message = discord.Embed()

        if player is None:
            embed_message.set_author(name="No Voice Connection")

            embed_message.add_field(name=f"🔇 There's no active voice connection to pause.",
                                    value="", inline=False)
            embed_message.add_field(name="What can you do?",
                                    value="", inline=False)
            embed_message.add_field(name="",
                                    value=f"- Want to start a music session?"
                                          f"Use the play command to get the party started!",
                                    inline=False)
            embed_message.add_field(name="",
                                    value=f"- Looking for more commands?"
                                          f"Type !help to explore all the available options.",
                                    inline=False)

            embed_message.colour = discord.Colour.dark_red()

            await ctx.send(embed=embed_message)
            return

        current_queue = player.current_queue()

        if not len(current_queue) > 1:
            embed_message.set_author(name=f"Queue Empty")

            embed_message.add_field(name=f"🎶 The music queue is currently empty and the stage awaits your command!",
                                    value="", inline=False)
            embed_message.add_field(name=f"🎙️ Ready to rock?",
                                    value="Fill the queue with your favorite tunes and let the music magic begin!",
                                    inline=False)

            embed_message.colour = discord.Colour.dark_grey()
        else:
            embed_message.set_author(name=f"Queue Overview")

            embed_message.title = f"🎶 Here's what's lined up in your music queue:"

            embed_message.description = ''
            for index, source in enumerate(current_queue[1:]):
                embed_message.description += f'**{index + 1}**. [{source.song.title}]({source.song.url})\n\n'
            embed_message.colour = discord.Colour.dark_grey()
        await ctx.send(embed=embed_message)

    @commands.command()
    async def skip(self, ctx: discord.ext.commands.Context):
        """
        Skips the current song and moves to the next song in the queue.

        Args:
            ctx:    :class:`discord.ext.commands.Context`: The context of the command invocation.

        """

        player = player_handler.get_player(ctx)
        embed_message = discord.Embed()

        if player and player.voice.is_playing():
            song = await player.skip()
            skipped_song = player.handler.queue[ctx.guild][0].song

            if song:
                embed_message.set_author(name="Song Skipped")

                embed_message.add_field(name="",
                                        value=f"⏭️ [{skipped_song.title}]({skipped_song.url}) by "
                                              f"[{skipped_song.channel}]({skipped_song.channel_url}) "
                                              f"has been gracefully skipped.",
                                        inline=False)
                embed_message.add_field(name="",
                                        value=f"🎵 Up next is [{song.title}]({song.url}) by"
                                              f"[{song.channel}]({song.channel_url})",
                                        inline=False)
                embed_message.add_field(name=f"🎧 Check out the queue with the queue command"
                                             f"to see what's lined up next.",
                                        value="", inline=False)

                embed_message.colour = discord.Colour.dark_blue()
            else:
                embed_message.set_author(name="No Songs to Skip")

                embed_message.add_field(name="⏭️ There are no songs in the queue to skip to.",
                                        value="",
                                        inline=False)
                embed_message.add_field(name=f"🎧 Ready to fill the queue with your favorite tunes?"
                                             f"Use the play command to get started!",
                                        value="", inline=False)

                embed_message.colour = discord.Colour.dark_blue()
        else:
            embed_message.set_author(name="No Voice Connection")

            embed_message.add_field(name=f"🔇 There's no active voice connection. There is no song to skip to.",
                                    value="", inline=False)
            embed_message.add_field(name="What can you do?",
                                    value="", inline=False)
            embed_message.add_field(name="",
                                    value=f"- Want to start a music session? "
                                          f"Use the play command to get the party started!",
                                    inline=False)
            embed_message.add_field(name="",
                                    value=f"- Looking for more commands?"
                                          f"Type !help to explore all the available options.",
                                    inline=False)

            embed_message.colour = discord.Colour.dark_red()

        await ctx.send(embed=embed_message)

    @commands.command(aliases=["np"], help="Shows the current playing song")
    async def now_playing(self, ctx: discord.ext.commands.Context):
        """
       Displays information about the currently playing song.

       Args:
           ctx:    :class:`discord.ext.commands.Context`: The context of the command invocation.

       """

        player = player_handler.get_player(ctx)
        embed_message = discord.Embed()

        if player is None:
            embed_message.set_author(name="No Voice Connection")

            embed_message.add_field(name=f"🔇 There's no active voice connection to be playing a song.",
                                    value="", inline=False)
            embed_message.add_field(name="What can you do?",
                                    value="", inline=False)
            embed_message.add_field(name="",
                                    value=f"- Want to start a music session? "
                                          f"Use the play command to get the party started!",
                                    inline=False)
            embed_message.add_field(name="",
                                    value=f"- Looking for more commands? "
                                          f"Type !help to explore all the available options.",
                                    inline=False)

            embed_message.colour = discord.Colour.dark_red()
            await ctx.send(embed=embed_message)
            return

        source = player.now_playing()

        if source is None:
            embed_message.set_author(name="Nothing is Playing")

            embed_message.add_field(name=f"The music station is currently silent "
                                         f"and there are no songs in the airwaves.",
                                    value="", inline=False)
            embed_message.add_field(name="🎧 Get ready to bring the rhythm back with the play command!",
                                    value="", inline=False)

            embed_message.colour = discord.Colour.dark_grey()
        else:
            embed_message.set_author(name=f'Currently playing:')
            embed_message.set_thumbnail(url=source.song.thumbnail)

            embed_message.title = f"{source.song.title} - ({source.song.duration})"
            embed_message.url = source.song.url

            embed_message.add_field(name="By",
                                    value=f"[{source.song.channel}]({source.song.channel_url})", inline=False)
            embed_message.add_field(name="Likes",
                                    value=f":thumbup: {source.song.likes}", inline=True)
            embed_message.add_field(name="Views",
                                    value=f":eye: {source.song.views}", inline=True)
            embed_message.add_field(name="Uploaded",
                                    value=f":date: "
                                          f"{datetime.strptime(source.song.date, '%Y%m%d').strftime('%Y/%m/%d')}",
                                    inline=False)
            requester_mention = source.song.requester.mention if source.song.requester is not None else ''
            embed_message.add_field(name="Requested By:",
                                    value=f"{requester_mention}", inline=False)
            delta_time = str((datetime.now() - source.song.start_time))
            completed_percentage =\
                (round((datetime.now() - source.song.start_time).total_seconds()) / source.song.duration_seconds * 100)
            completed_song: int
            completed_song = math.ceil(completed_percentage) // 10
            formatted_time = datetime.strptime(delta_time, '%H:%M:%S.%f').strftime('%H:%M:%S')
            embed_message.add_field(name="Playback Position",
                                    value=f":arrow_forward: "
                                          f"{formatted_time} - "
                                          f"[{completed_song * ' ⬜ '}{(10 - completed_song) * ' ⬛ '}] "
                                          f"- {source.song.duration}", inline=False)
            next_song = player.handler.queue[ctx.guild][1] if len(player.handler.queue[ctx.guild]) > 1 else None

            if next_song is not None:
                embed_message.add_field(name="Next",
                                        value=f":track_next: {next_song.song.title}", inline=False)
            else:
                embed_message.add_field(name="Next",
                                        value=f":no_entry: Nothing left in the queue", inline=False)

            embed_message.colour = discord.Colour.dark_grey()

        await ctx.send(embed=embed_message)

    @commands.command()
    async def remove(self, ctx: discord.ext.commands.Context, *, index: int):
        """
        Removes a song from the queue.

        Args:
            ctx:    :class:`discord.ext.commands.Context`: The context of the command invocation.
            index:  :class:`str`: The index of the song to be removed.

        """

        player = player_handler.get_player(ctx)
        embed_message = discord.Embed()

        if player is None:
            embed_message.set_author(name="No Voice Connection")

            embed_message.add_field(name=f"🔇 There's no active voice connection. There is no queue to remove from.",
                                    value="", inline=False)
            embed_message.add_field(name="What can you do?",
                                    value="", inline=False)
            embed_message.add_field(name="",
                                    value=f"- Want to start a music session? "
                                          f"Use the play command to get the party started!",
                                    inline=False)
            embed_message.add_field(name="",
                                    value=f"- Looking for more commands?"
                                          f"Type !help to explore all the available options.",
                                    inline=False)

            embed_message.colour = discord.Colour.dark_red()
            await ctx.send(embed=embed_message)
            return

        current_queue = player.current_queue()
        if len(current_queue) <= 1:
            embed_message.set_author(name="Nothing to Remove")

            embed_message.add_field(name=":wastebasket: The queue is currently empty and there are no songs to remove.",
                                    value="",
                                    inline=False)
            embed_message.add_field(name=f"🎧 Ready to add your favorite songs to the queue?"
                                         f"Use the play command to get started!",
                                    value="", inline=False)

            embed_message.colour = discord.Colour.dark_blue()
        else:
            song = await player.remove(index=index)

            embed_message.set_author(name="Song Removed")

            embed_message.add_field(name="",
                                    value=f":wastebasket: [{song.title}]({song.url}) by "
                                          f"[{song.channel}]({song.channel_url}) has been removed from the queue",
                                    inline=False)
            embed_message.add_field(name=f"🎧 Curious about what's up next?"
                                         f"Check out the queue with the queue command!",
                                    value="", inline=False)

            embed_message.colour = discord.Colour.dark_blue()

        await ctx.send(embed=embed_message)

    @play.before_invoke
    async def ensure_voice(self, ctx: discord.ext.commands.Context):
        """
        Ensures that the bot is in a voice channel before executing a music-related command.

        Args:
            ctx:    :class:`discord.ext.commands.Context`: The context of the command invocation.

        """

        embed_message = discord.Embed()

        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                embed_message.description = ":exclamation::exclamation:You must be in a voice " \
                                            "channel:exclamation::exclamation: "
                embed_message.colour = discord.Colour.dark_red()
                await ctx.send(embed=embed_message)


async def setup(bot):
    await bot.add_cog(Music(bot))
