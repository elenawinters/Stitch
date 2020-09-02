#
#   Developed by Elena Winters (ElenaBerry#2561), aka Tracer
#   Contributions by: Raine Bannister and RingoMar
#
#   This bot is used and hosted by me (Elena), for others to use.
#
#

from core.color import trace
from core.logger import log
from core import manager
from core import utils
from data import data
from core import web
import core.json
import threading
import datetime
import extends
import debug
import time
import sys


if __name__ == '__main__':
    extends.Initialize()
    debug.Initialize()

    data.Initialize()

    threads = manager.Initialize().threads

    host = core.json.orm['api']
    core.web.Client(f"http://{host['host']}:{host['port']}/uptime/").post({'uptime': str(datetime.datetime.utcnow())})

    log.debug(f'Current threads: {threads}')

    while all(x.is_alive() for x in threads):
        time.sleep(2)

    uptime = (core.web.Client(f"http://{host['host']}:{host['port']}/uptime/").get()).json()
    log.debug(uptime)

    sys.exit(0)
