import discord
from discord.ext import commands
from func.funcs import log, error, warn
from func.tools import tls
from func import json


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_resumed(self):
        pass


def setup(bot):
    bot.add_cog(General(bot))

