#
#   Developed by Elena Winters (ElenaBerry#2561), aka Tracer
#   Contributions by: Raine Bannister and RingoMar
#
#   This bot is used and hosted by me (Elena), for others to use.
#
#   Codename: .tls
#   Display: Purpose
#

from core.color import trace
from data.data import data
from core.bot.tools import *
from core.logger import log
from core.bot.time import Time
import traceback
import asyncio
import session
import sys


if __name__ == '__main__':
    log.info(f'>{trace.cyan} Starting at {Time.readable.at()}.')
    # Initialize database
    log.info(f'{trace.cyan}> Initializing {trace.black.s}dataset{trace.cyan} Database.')
    try:
        data()
        log.info(f'{trace.cyan}> Initialized {trace.black.s}dataset{trace.cyan}.')
    except Exception as err:
        log.warning(f'> Failed to load {trace.black.s}dataset{trace.warn}. Please restart!')
        log.error(f'> {short_traceback()}')
        log.critical(f'> {traceback.format_exc()}')

    # Start API
    import api
    api.Main()

    # Initialize extensions
    # Append cCogs
    # append_cog('session.py')  # Load session
    append_cog('debug.py')  # Load debug things
    append_cog('main.py')  # Load essentials

    # Login
    from core.bot import time
    time.uptime = datetime.datetime.utcnow()

    from core.bot import login
    threads = login.LoginManager(prefix='.').login()
    t_count = 0
    for t in threads:
        # login.time.sleep(2)
        t_count += 1
        t.name = f'Discord-{t_count}'
        t.start()
    # [t.start() for t in threads]
    while all(x.is_alive() for x in threads):
        login.time.sleep(2)
    log.info('Bot is shutting down')
    log.info(f'> Uptime: {Time.uptime(Time())}')
    sys.exit()
