import discord
from discord.ext import commands

from func.color import trace
from func.funcs import *
from data.data import data

class filters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # print(message.content)
        pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, message):
        # print(message.content)
        pass


def setup(bot):
    bot.add_cog(filters(bot))
