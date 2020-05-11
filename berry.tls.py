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
client2 = commands.Bot(command_prefix='.')

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
    append_cog('debug.py')  # Load debug things
    append_cog('main.py')  # Load essentials

    # Login
    time.uptime = datetime.datetime.utcnow()

    try:
        from core.bot.login import *
        threads = LoginManager(prefix='.').login()
        import time
        while True:
            time.sleep(2)
            if not threads[0].is_alive():
                break
            if core.flags.restart:
                break
    except KeyboardInterrupt:
        sys.exit('Closed')
    except Exception as err:
        log.exception(err)

log.info(f'> Uptime: {Time.uptime(Time())}')
