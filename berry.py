"""
    Developed by Elena Winters (Winters#2561), aka Tracer
    Contributions by: Raine Bannister and RingoMar

    This bot is used and hosted by me (Elena), for others to use.

"""

from core.logger import log, trace, json
from dateutil import parser
from core import manager
from core import util
from core import web
import importlib
import threading
import datetime
import asyncio
import debug
import time
import sys
import os


def berry(**kwargs):
    log.debug(f"{util.crypt('weeeeee')}")

    asyncio.set_event_loop(asyncio.new_event_loop())

    # Start threads
    threads = manager.Initialize().threads
    log.debug(f'Current threads: {threads}')

    web.api('uptime').post(json={'uptime': str(datetime.datetime.utcnow())})
    web.api('gating').post(json=kwargs)

    # host = json.orm['api']  # Post current time to api)
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


def start(**kwargs):
    """
        This function runs the berry function on a loop.

        We use a print function instead of ctypes for setting a title
        because it's claimed to work on every system (untested).

    """

    log.debug(sys.version)

    name = json.orm['name']
    title = f'| {name}'

    print(f"\033]0;{title}\007", flush='', end='')  # this apparently works on all systems?

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    while True:
        try:
            t = threading.Thread(target=berry, name=name, kwargs=kwargs, daemon=True)
            t.start()  # Starts thread
            t.join()  # Waits for completion
        except Exception as exc:
            log.exception(exc)


if __name__ == '__main__':
    start()
