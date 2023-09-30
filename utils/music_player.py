from __future__ import annotations

from typing import List

from utils import ytdl_utils

import asyncio
import datetime

import discord
from discord.ext import commands


class NotConnectedToVoice(Exception):
    """Cannot create the player because the bot is not connected to voice"""


class NotPlaying(Exception):
    """Nothing is playing"""


class EmptyQueue(Exception):
    """The queue is empty"""


class PlayerHandler:
    def __init__(self):
        self.queue: dict[discord.ext.commands.Context.guild, list[ytdl_utils.YTDLSource]] = {}
        self.players: dict[discord.ext.commands.Context.guild, MusicPlayer] = {}

    def create_player(self, ctx: discord.ext.commands.Context, **kwargs) -> MusicPlayer:
        if not ctx.voice_client:
            raise NotConnectedToVoice("Cannot create the player because the bot is not connected to voice")

        player = MusicPlayer(ctx, self, **kwargs)
        self.players[ctx.guild] = player

        return player

    def get_player(self, ctx: discord.ext.commands.Context) -> MusicPlayer | None:
        if ctx.guild not in self.players:
            return None

        return self.players[ctx.guild]


class MusicPlayer:
    def __init__(self, ctx: discord.ext.commands.Context, handler: PlayerHandler, **kwargs):
        self.ctx = ctx
        self.voice = ctx.voice_client
        self.guild = ctx.guild
        self.ffmpeg_options = kwargs.get("ffmpeg_options")
        self.handler = handler

        if self.guild not in self.handler.queue:
            self.handler.queue[self.guild]: list[ytdl_utils.YTDLSource] = []

    async def _check_queue(self):
        try:
            self.handler.queue[self.guild].pop(0)
        except IndexError:
            raise EmptyQueue

        try:
            source = self.handler.queue[self.guild][0]
            source.song.start_time = datetime.datetime.now()
            self.voice.play(source,
                            after=lambda e: asyncio.run_coroutine_threadsafe(
                                self._check_queue(),
                                self.ctx.bot.loop
                            ) if not e else e)
        except IndexError:
            return

    async def play(self) -> ytdl_utils.Song:
        source = self.handler.queue[self.guild][0]

        self.voice.play(source,
                        after=lambda e: asyncio.run_coroutine_threadsafe(
                            self._check_queue(),
                            self.ctx.bot.loop
                        ) if not e else e)

        return source.song

    async def stop(self):
        try:
            self.voice.stop()
            self.handler.queue[self.guild].clear()
        except self.handler.queue[self.guild] == []:
            raise NotPlaying("Nothing is playing")

    async def resume(self) -> ytdl_utils.Song:
        try:
            self.voice.resume()
            source = self.handler.queue[self.guild][0]
        except self.handler.queue[self.guild] == []:
            raise NotPlaying("Nothing is playing")

        return source.song

    async def pause(self) -> ytdl_utils.Song:
        try:
            self.voice.pause()
            source = self.handler.queue[self.guild][0]
        except self.handler.queue[self.guild] == []:
            raise NotPlaying("Nothing is playing")

        return source.song

    async def queue(self, url) -> ytdl_utils.Song:
        source = await ytdl_utils.YTDLSource.fetch_video_data(url, self.ctx.bot.loop, requester=self.ctx.author)
        self.handler.queue[self.guild].append(source)

        return source.song

    async def skip(self) -> ytdl_utils.Song | None:
        if len(self.handler.queue[self.guild]) > 1:
            try:
                self.voice.stop()

                return self.handler.queue[self.guild][1].song
            except IndexError:
                return None

    async def remove(self, index=0) -> ytdl_utils.Song:
        try:
            song = self.handler.queue[self.guild][index].song
        except IndexError:
            raise NotPlaying("Nothing is playing")

        if index == 0:
            await self.skip()

        return song

    def now_playing(self):
        try:
            return self.handler.queue[self.guild][0]
        except KeyError:
            return None
        except IndexError:
            return None

    def current_queue(self):
        try:
            return self.handler.queue[self.guild]
        except KeyError:
            raise EmptyQueue("The queue is empty")
