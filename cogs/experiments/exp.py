import discord
from discord.ext import commands
from core.bot import settings
from core.bot import perms
from core.color import trace
from core.bot import tools
# from core.bot.funcs import *
from core.bot import enums
from core.ext.enums import general
from core import json
import traceback
import requests
from core.ext import assets
from core.bot.time import time
import colorsys
import asyncio
from core.logger import log
import re


class Experiments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     raise Exception('Test error')

    @commands.group(name='test')
    @settings.enabled()
    @perms.subcommand()
    async def test(self, ctx):
        # Actively test things
        if not ctx.invoked_subcommand:
            for x in self.bot.extensions:
                print(x)
            # t = f"{trace.alert}This {trace.cyan}is a {trace.yellow.s}TEST{trace.alert} string!"
            # log.info('test')
            # log.debug(f'{t}: debug')
            # log.info(f'{t}: info')
            # log.warn(f'{t}: warn')
            # log.error(f'{t}: error')
            # log.critical(f'{t}: critical')
            # import logging
            # print(logging.LogRecord.message)
            # print(type(trace.tracers))
            # def sub(m):
            #     return '' if m.group() in trace.tracers else m.group()
            # out = re.sub(r'\w+', sub, t_string)
            # print(t_string)
            # print(out)
            # def t_filter(obj):
            #     if (i for i in trace.tracers if i not in obj):
            #         return True
            #     else:
            #         return False
            # out = list(filter(t_filter , t_string.split(' ')))

            # for x in out:
            #     print(x)
            # print(out)
            # print(''.join([str(elem) for elem in out]))
            pass

    # @test.command()
    # @perms.is_admin()
    # async def welcome(self, ctx, guid=None):
    #     await welcome_message(ctx.author, bot=self.bot, guid=guid)

    @test.command(aliases=['err'])
    @commands.is_owner()
    async def error(self, ctx, guid=None):
        raise Exception('This is a test error')

    @test.command(aliases=['err2', 'log_error', 'log_err'])
    @commands.is_owner()
    async def error2(self, ctx, guid=None):
        log.info('Hello', 9999)

    @test.command(name='color', aliases=['colors', 'colour', 'colours', 'c'])
    @commands.is_owner()
    async def colors(self, ctx, *, text='Test message for color example.'):
        for x in trace.tracers:  # This does not get logged to the log.txt
            print(f'{trace.reset}{x}{text}{trace.reset}')


def setup(bot):
    bot.add_cog(Experiments(bot))

