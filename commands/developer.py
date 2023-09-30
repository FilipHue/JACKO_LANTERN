import discord
from discord.ext import commands


class DeveloperUtils(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(help="Loads an extension")
    @commands.has_permissions(administrator=True)
    async def load(self, ctx: commands.Context, extension: str):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await self.bot.load_extension(f"commands.{extension}")
        await ctx.send(f"Loaded extension {extension}")

    @commands.command(help="Unloads an extension")
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx: commands.Context, extension: str):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await self.bot.unload_extension(f"commands.{extension}")
        await ctx.send(f"Unloaded extension {extension}")

    @commands.command(help="Reloads an extension")
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx: commands.Context, extension: str):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await self.bot.unload_extension(f"commands.{extension}")
        await self.bot.load_extension(f"commands.{extension}")
        await ctx.send(f"Reloaded extension {extension}")


async def setup(bot):
    await bot.add_cog(DeveloperUtils(bot))
