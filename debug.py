import discord
from discord.ext import commands
# from core.bot.funcs import *
from core.logger import log
from core.color import trace
from core.bot.tools import *
from core.bot import enums
test = False


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        if not self.bot.is_ready():
            log.info(f'{trace.cyan}> Logging in at {time.readable.at()}.')
        else:
            log.debug(f'{trace.cyan}> Connection with {trace.white}Discord{trace.cyan} achieved.')

    @commands.Cog.listener()
    async def on_disconnect(self):
        if test:
            log.debug(f'{trace.cyan}> Connection with {trace.white}Discord{trace.cyan} lost.')

    @commands.Cog.listener()
    async def on_resumed(self):
        if test:
            log.debug(f'{trace.cyan}> Connection with {trace.white}Discord{trace.cyan} resumed.')


def setup(bot):
    bot.add_cog(Debug(bot))
