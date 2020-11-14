#
#   Developed by Elena Winters (ElenaBerry#2561), aka Tracer
#   Contributions by: Raine Bannister and RingoMar
#
#   This bot is used and hosted by me (Elena), for others to use.
#
#

from core.logger import log, trace, json
from dateutil import parser
from core import manager
from core import utils
from core import web
import importlib
import threading
import datetime
import asyncio
import debug
import time
import sys


def start():
    asyncio.set_event_loop(asyncio.new_event_loop())
    # queue.assign([])  # Create queue

    # Start threads
    threads = manager.Initialize().threads
    log.debug(f'Current threads: {threads}')

    web.api('uptime').post({'uptime': str(datetime.datetime.utcnow())})

    # host = json.orm['api']  # Post current time to api
    # web.Client(f"http://127.0.0.7:5009/utime/").post({'uptime': str(datetime.datetime.utcnow())})  # Will error
    # web.Client(f"http://{host['host']}:{host['port']}/uptime/").post({'uptime': str(datetime.datetime.utcnow())})

    debug.Initialize()  # Run debugging functions
    if len(threads) > 0:
        while all(x.is_alive() for x in threads):  # Kill program if a thread dies
            # log.debug(queue())
            time.sleep(2)

        # Log which threads died
        [log.debug(f'{trace.warn}Thread "{x.name}" has died.') for x in threads if not x.is_alive()]

    # uptime = web.Client(f"http://{host['host']}:{host['port']}/uptime/").get()
    # log.debug(parser.parse(uptime.json()['uptime']))

    sys.exit(0)


if __name__ == '__main__':
    start()
