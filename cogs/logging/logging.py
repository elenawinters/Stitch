import discord
from discord.ext import commands
import sys, traceback

from func.color import trace
from func.funcs import log, error
from func.funcs import extensions
from func import enums


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_server_join(self, server):
        log(f'> Joined {server.name}', enums.LogLevel.default)

    @commands.Cog.listener()
    async def on_server_remove(self, server):
        error(f'> Removed from {server.name}', enums.LogLevel.default)


def setup(bot):
    bot.add_cog(Logs(bot))
