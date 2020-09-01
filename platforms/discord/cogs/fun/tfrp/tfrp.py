import discord
from discord.ext import commands
from core.ext.enums import general
from core.bot.tools import tls
from core.bot import tools
from core.logger import log
import httpx as requests
import core.bot.perms
import datetime
import random


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['fam', 'thefam', 'thefamilyrp', 'thefamrp', 'famrp', 'familyrp'])
    async def tfrp(self, ctx):
        if not ctx.invoked_subcommand:
            pass

    @tfrp.command()
    async def perma(self, ctx):
        pass

    @tfrp.command(name='firebug')
    @commands.is_owner()
    async def firebug_generator(self, ctx, *, text):
        colors = ['^1', '^3', '^8', '^9', '^7']
        output = gen(colors, text, bold=True)
        await ctx.send(f'```{output}```')

    @tfrp.command(name='capitan', aliases=['lola', 'vue'])
    @commands.is_owner()
    async def lola_generator(self, ctx, *, text):
        colors = ['^0', '^7', '^6', '^5']
        output = gen(colors, text, bold=False)
        await ctx.send(f'```{output}```')


def setup(bot):
    bot.add_cog(Fun(bot))


def gen(colors, text, bold=False):
    if bold:
        output = ['^*']
    else:
        output = ['']
    for x in text:
        if x != ' ':
            if len(output) > 1:
                pick = random.choice(colors)
                if output[-2] in colors:
                    if pick != output[-2]:
                        output.append(pick)
                else:
                    output.append(random.choice(colors))
            else:
                output.append(random.choice(colors))
        output.append(x)
    output.append('^r')
    output = ''.join(output)
    return output
