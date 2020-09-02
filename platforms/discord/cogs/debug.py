import discord
from discord.ext import commands
# from core.bot.funcs import *
from core.color import trace
from core import logger
from core import json


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.is_owner()
    # async def test(self, ctx):
    #     logger.json
    #     logger.json.load("application\\api\\ext\\ban_assist.json")
    #     logger.json.load("test.json")

    @commands.Cog.listener()
    async def on_connect(self):
        if not self.bot.is_ready():
            logger.log.info(f'{trace.cyan}> Logging in at {time.readable.at()}.')
        else:
            logger.log.debug(f'{trace.cyan}> Connection with {trace.white}Discord{trace.cyan} achieved.')


def setup(bot):
    bot.add_cog(Debug(bot))
