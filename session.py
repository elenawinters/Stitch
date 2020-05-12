import discord
from discord.ext import commands
from core.color import trace
from core.logger import log
import aiohttp
session = type(aiohttp.client)


class Stitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await cleanup()
        global session
        connector = aiohttp.TCPConnector(limit=60)
        session = aiohttp.ClientSession(connector=connector)


def setup(bot):
    bot.add_cog(Stitch(bot))


async def cleanup():
    try:
        await session.close()
    except Exception:
        pass
