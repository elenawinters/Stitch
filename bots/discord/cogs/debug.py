import discord
from discord.ext import commands
from ..core import decorators
from ..core.tools import tls
from core.logger import log
from core import json


# Use this to prototype
class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @decorators.permissions(0)
    async def test(self, ctx):
        async for x in ctx.message.channel.history(limit=500):
            log.debug(x.content)
            if x.content == 't':
                log.debug('breaking')
                break
        log.debug('broke')


def setup(bot):
    bot.add_cog(Debug(bot))
