import discord
from discord.ext import commands
from ..core import predicates
from ..core.tools import tls
from core import logger
from core import json


# Use this to prototype
class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.is_owner()
    @predicates.manager()
    async def test(self, ctx):
        logger.json
        logger.json.load("application\\api\\ext\\ban_assist.json")
        logger.json.load("test.json")


def setup(bot):
    bot.add_cog(Debug(bot))
