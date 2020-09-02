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
from core import utils
from core import web
import core.json
import threading
import datetime
import extends
import sys


# Exception hook
def hook(exctype, value, tb):
    log.exception(**utils.Utils().Traceback((exctype, value, tb)).code())


threading.excepthook = hook
sys.excepthook = hook

if __name__ == '__main__':
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

    extends.Initialize()

    from core import manager
    threads = manager.Initialize().threads

    # import time
    # return time.strftime("%X", time.localtime(time.time()))

    host = core.json.json.orm['api']
    core.web.Client(f"http://{host['host']}:{host['port']}/uptime/").post({'uptime': str(datetime.datetime.utcnow())})

    log.debug(f'Current threads: {threads}')

    # for x in threads:
    #     log.debug(x.name)

    import time
    while all(x.is_alive() for x in threads):
        time.sleep(2)

    uptime = (core.web.Client(f"http://{host['host']}:{host['port']}/uptime/").get()).json()
    log.debug(uptime)
    # log.info(f"> Uptime: {uptime.json['uptime']}")

    sys.exit(0)
