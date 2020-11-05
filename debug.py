from core.queue import queue
from core.logger import log
from core.utils import util
from dateutil import parser
from core import web, json
import threading
import string
import random
import time
import sys


# https://stackoverflow.com/a/3467879/14125122
class Initialize():  # Runtime debug
    def __init__(self):
        for run in util.hack_the_planet():
            run(self)
        # funcs = util.hack_the_planet()
        # [threading.Thread(target=funcs[x], args=(self,), daemon=True, name=f'Debug-{x+1}').start() for x in range(len(funcs))]

    def z_exit(self):  # If this is uncommented, it kills the program after all debug functions have run
        sys.exit(0)

    def tests(self):
        log.debug('Nothing to test!')

    # def test1(self):
    #     test = {letter: f'{index:02d}' for index, letter in enumerate(string.ascii_lowercase, start=1)}
    #     pass
