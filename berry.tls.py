#
#   Developed by Elena Winters (ElenaBerry#2561), aka Tracer
#   Contributions by: Raine Bannister
#
#   This bot is used and hosted by me (Elena), for others to use.
#
#   Codename: .tls
#   Display: Purpose
#

# This is required. Settings file will be wiped if this is not here
# from core.defaults import setup
# setup.startup()  # Run startup

from core.bot.funcs import extensions
from discord.ext import commands
# from core.defaults import setup
from core.color import trace
from data.data import data
from core.bot.funcs import respond
from core.bot.login import Login
from core.bot.tools import *
from core.logger import log
from core.bot import enums
from threading import Thread
from core.bot.time import Time
from core.bot import time
from core import json
import core.flags
import traceback
# import colorama
import asyncio
import discord
import ast
import sys
# colorama.init()
# setup.startup()
client = commands.Bot(command_prefix='.')
# client2 = commands.Bot(command_prefix='.')
custom_help = True
if custom_help:
    client.remove_command('help')


@client.event
async def on_ready():
    log.info(f'{trace.cyan}> Logged in: {trace.yellow.s}{client.user.name}, {trace.cyan.s}{client.user.id}, {trace.magenta.s}Initiated.')


@client.event
async def on_command(ctx):
    try:
        await ctx.message.delete()
    except Exception:
        pass


if __name__ == '__main__':
    log.info(f'>{trace.cyan} Starting at {time.time.readable.at()}.')
    # Initialize database
    log.info(f'{trace.cyan}> Initializing {trace.black.s}dataset{trace.cyan} Database.')
    try:
        data()
        log.info(f'{trace.cyan}> Initialized {trace.black.s}dataset{trace.cyan}.')
    except Exception as err:
        log.warning(f'> Failed to load {trace.black.s}dataset{trace.warn}. Please restart!')
        log.error(f'> {short_traceback()}')
        log.critical(f'> {traceback.format_exc()}')

    # Initialize extensions
    # Append cCogs
    append_cog('errors.py')  # Load error handlers
    append_cog('debug.py')  # Load debug things

    import loader
    loader.Load(client).run()
    # loader.Load(client2).run()

    # Login
    time.uptime = datetime.datetime.utcnow()

    try:
        from core.bot.login import *
        Login(client)
        import time
        while True:
            time.sleep(2)
            if core.flags.restart:
                break
    except KeyboardInterrupt:
        sys.exit('Closed')
    except Exception as err:
        log.exception(err)

log.info(f'> Uptime: {Time.uptime(Time())}')
