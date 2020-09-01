import discord
from discord.ext import commands
from core.bot import settings
from core.bot import perms
from core.color import trace
from core.bot import funcs
from core.bot import tools
from core.bot import enums
from core.ext.enums import general
import core.json
import json
import traceback
from core.ext import assets
from core.bot.time import time
import colorsys
import asyncio
from core.bot import funcs
from core.logger import log
from data.data import data
import core.checks
import core.web
import importlib
import httpx
import sys
import ast
import re
import os


class Experiments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        log.debug('Cog was unloaded')

    @commands.group(name='test')
    @settings.enabled()
    @perms.subcommand()
    @core.checks.is_banned()
    async def test(self, ctx):
        # Actively test things
        if not ctx.invoked_subcommand:
            d1 = {
                'testing': 'This is test command 1'
            }
            d2 = {
                'test': 'This is test command 2'
            }
            core.json.json.merge(d1, d2)
            # log.debug(d1)
            # log.debug(d1.pop)
            d1[('test', 'test2', 'tart')] = d1.pop(('test'))
            # v = [v for k, v in d1 if 'test' in k]
            # log.debug(v)

            def match(obj, find):  # Returns key, you can match the key with the dict to get the value
                for k, v in d1.items():
                    if isinstance(k, str):
                        if find == k:
                            return k
                    else:
                        for x in k:
                            if find == x:
                                return k
                return None

            # log.debug('here')
            t = match(d1, 'testing')
            # log.debug('here2')
            # log.debug(t)
            log.debug(d1[t])
            # t = [{k: v} for k, v in d1.items() for item in k if 'test' == item][0]
            # log.debug(t)
            # log.debug(d1)
            # test
            # try:
            #     # raise KeyError
            #     raise Exception('This is a test error')
            # except Exception as exc:
            #     log.exception(**tools.tls.Traceback(exc).code())

            # t = data.base['bans'].all()
            # log.debug(t)
            # b = {}
            # for x in t:
            #     b.update({x['id']: {
            #         'reason': x['reason'],
            #         'date': x['date'],
            #         'by': x['by'],
            #     }})
            # log.debug(b)

            # r = await core.checks.ban_assistants()
            # r = await core.web.Request('http://localhost:5001/stat/').async_get()
            # log.debug(r)

            # send = {
            #     self.bot.user.id: self.bot.user.name
            # }

            # async with httpx.AsyncClient() as client:
            #     await client.post(url='http://localhost:5001/stat/post', json=dict(send))
            # ban = data.base['bans'].find_one(id=141802236861743104)
            # log.debug(ban)
            # json.json.ORM('test.json')['test'] = 1
            # log.debug(json.json.ORM('test.json')['test'])
            # while True:
            #     try:
            #         log.debug(ctx.me.guild.voice_client.timestamp)
            #     except Exception:
            #         pass
            #     await asyncio.sleep(2)
            # src = ctx.me.guild.voice_client.source
            # log.debug(src)
            # for x in self.bot.extensions:
            #     log.debug(x)

            # log.debug('test')
            # abspath = os.path.abspath('.')
            # for x in funcs.extensions():
            #     cog = importlib.import_module(x, abspath)
            #     await cog.cleanup()
            # log.debug(json.json.orm['activity'].get(str(self.bot.user.id)))
            # import sys
            # sys.exit('Burn it with fire')
            # roles = [706752710896123934, 706752711541915719, 706752713353855108]
            # other = [Snowflake(r) for r in roles]
            # for x in other:
            #     log.debug(x.id)
            # other = [1, 706752711541915719, 95446564632514]
            # roles = [Snowflake(706752710896123934), Snowflake(706752711541915719), Snowflake(706752713353855108)]
            # other = [1, 706752711541915719, 95446564632514]
            # out = [i.id for i, j in zip(roles, other) if i.id == j]
            # log.debug(out)
            #
            # for x in ctx.author.roles:
            #     log.debug(f'{type(x)}: {x.id}')

            # roles_list = [Snowflake(706752710896123934), Snowflake(706752711541915719), Snowflake(706752713353855108)]
            # for x in roles_list:
            #     for y in ctx.author.roles:
            #         if y.id == x.id:
            #             log.debug(y)
            # roles = [y for y in ctx.author.roles for x in roles_list if y.id == x.id]
            # for x in roles:
            #     log.debug(x.id)
            # for x in ctx.author.roles:

            # for x in ctx.author.roles:
            #     log.debug(f'{type(x.id)}: {x.id}')
            # # log.debug(roles)
            # # log.debug(ctx.author.roles)
            # comp = [i.id for i, j in zip(roles, ctx.author.roles) if i.id == j.id]
            # log.debug(comp)
            # for x in roles:
            # log.debug(x.id)
            # await ctx.author.add_roles(*roles)

            # for r in ctx.author.roles:
            #     if r.id in [626258619779907595]:
            #         log.debug('Has role')
            #         break

            # from cogs.custom import cmus
            # bot = cmus.Player.self(self, ctx)
            # await cmus.Player.play.file('audio\\testing\\HEYEAYEA - The Soundcloud Meta Edition-146792980.mp3', bot)
            # bot.guild.voice_client.play(audio)

            # DANGEROUS CODE
            # DO NOT RUN
            # audio = discord.FFmpegPCMAudio(source=path)
            # discord.player.AudioPlayer(source=audio, client=bot.guild.voice_client).run()

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
#
#
# async def unload():
#     log.debug('I HAVE BEEN UNLOADED')
