import discord
from discord.ext import commands
from ..core import decorators
from ..core.tools import tls
from core import logger
from core import json


# Use this to prototype
class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @decorators.permissions(0)
    async def test(self, ctx):
        logger.log.debug('Testing permissions')
        # logger.json.load("application\\api\\ext\\ban_assist.json")
        # logger.json.load("test.json")


def setup(bot):
    bot.add_cog(Debug(bot))
