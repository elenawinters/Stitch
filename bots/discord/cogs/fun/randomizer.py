import discord
from discord.ext import commands
from ...core import decorators
from ...core.tools import tls
from core.logger import log
import random


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='word', aliases=['words'])
    @decorators.banned()
    async def random_words(self, ctx: commands.Context, *, phrase: str = None):
        phrase = phrase.split(' ')
        random.shuffle(phrase)
        await ctx.send(' '.join(phrase))

    @commands.command(name='drow', aliases=['drows'])
    @decorators.banned()
    async def random_drows(self, ctx: commands.Context, *, phrase: str = None):
        phrase = list(phrase)
        random.shuffle(phrase)
        await ctx.send(''.join(phrase))


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
