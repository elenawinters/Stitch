""" REFERENCE guilds.pyw FOR OLD CODE """

import discord
from core.logger import log
from discord.ext import commands
from ...core.tools import tls
from core import web


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def settings(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass


def setup(bot):
    bot.add_cog(Settings(bot))
