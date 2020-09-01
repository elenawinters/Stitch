#
#   Developed by Elena Winters (ElenaBerry#2561), aka Tracer
#   Contributions by: Raine Bannister and RingoMar
#
#   This bot is used and hosted by me (Elena), for others to use.
#
#

from core.color import trace
from data.data import data
from core.bot.tools import *
from core.logger import log
from core.bot.time import Time
import traceback
import asyncio
import sys
import ast


if __name__ == '__main__':
    log.info(f'>{trace.cyan} Starting at {Time.readable.at()}.')
    # Initialize database (this needs to be improved)
    log.info(f'{trace.cyan}> Initializing {trace.black.s}dataset{trace.cyan} Database.')
    try:
        data()
        log.info(f'{trace.cyan}> Initialized {trace.black.s}dataset{trace.cyan} engine ({data.engine}).')
        # log.info(f'{trace.cyan}> Initialized {trace.black.s}dataset{trace.cyan}. Engine: {tracer.yellow.s}{}')
    except Exception as err:
        log.warning(f'> Failed to load {trace.black.s}dataset{trace.warn}. Restarting!')
        log.error(f'> {short_traceback()}')
        log.critical(f'> {traceback.format_exc()}')
        sys.exit(0)

    from core import manager
    threads = manager.Initialize().threads

    log.debug(f'Current threads: {threads}')

    # for x in threads:
    #     log.debug(x.name)

    import time
    while all(x.is_alive() for x in threads):
        time.sleep(2)
