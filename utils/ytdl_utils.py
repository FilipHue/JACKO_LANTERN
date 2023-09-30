import asyncio
import datetime
from pprint import pprint

import discord
import yt_dlp

ytdl_options = {
    "format": "bestaudio/best",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": True,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "source_address": "0.0.0.0"
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl_player = yt_dlp.YoutubeDL(ytdl_options)
ytdl_player.add_default_info_extractors()


class Song:
    def __init__(self, source, url, title, description, duration_seconds, thumbnail, likes, views,
                 duration, date, channel, channel_url, requester, loop):
        self.source = source
        self.url = url

        self.title = title
        self.description = description
        self.duration = duration
        self.duration_seconds = duration_seconds
        self.date = date

        self.likes = likes
        self.views = views

        self.thumbnail = thumbnail
        self.channel = channel
        self.channel_url = channel_url

        self.start_time = datetime.datetime.now()
        self.requester = requester
        self.is_looping = loop


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, song: Song, volume=0.5):
        super().__init__(source, volume)

        self.song = song

    @classmethod
    async def fetch_video_data(cls, url, loop=None, stream=True, requester=None):
        loop = loop or asyncio.get_event_loop()

        data = await loop.run_in_executor(None, lambda: ytdl_player.extract_info(url, download=not stream))
        # pprint(data)

        source = data["url"]
        url = "https://www.youtube.com/watch?v=" + data["id"]
        title = data["title"]
        description = data["description"]
        thumbnail = data["thumbnail"]
        likes = data["like_count"]
        views = data["view_count"]
        duration = data["duration_string"]
        duration_seconds = data["duration"]
        date = data["upload_date"]
        channel = data["uploader"]
        channel_url = data["uploader_url"]

        song = Song(
            source, url, title, description, duration_seconds, thumbnail, likes, views,
            duration, date, channel, channel_url, requester, loop)

        return cls(
            discord.FFmpegPCMAudio(source, **ffmpeg_options), song=song)

    def __getitem__(self, item):
        return self
