from core.logger import log, trace
from dateutil import parser
from core import web, json
from core import util
import threading
import string
import random
import time
import sys
# import ui


# https://stackoverflow.com/a/3467879/14125122
class Initialize():  # Runtime debug
    def __init__(self):
        if len(hacks := util.hack_the_planet()) > 0:
            web.api('gating/test').post(json=True)
            for run in hacks:
                run(self)
        else:
            log.debug('Nothing to test!')
        # funcs = util.hack_the_planet()
        # [threading.Thread(target=funcs[x], args=(self,), daemon=True, name=f'Debug-{x+1}').start() for x in range(len(funcs))]

    # def z_exit(self):  # If this is uncommented, it kills the program after all debug functions have run
    #     log.debug('Nothing to test!')
    #     sys.exit(0)

    def tests(self):
        # for x in range(0, 5):
        #     t = web.api('gating/ui').get().json()
        #     log.debug(t)
        if interface := web.api('gating/ui').get().json():
            log.debug(f'API indicates that the UI is active! (gating/ui: {interface})')
        # log.debug('Nothing to test!')
        # for x in trace.tracers:
        #     log.debug(f'{x}Hello world')

    # def test1(self):
    #     log.debug(f'{}Hello this is a test')

        # italics = '\033[3m'
        # underline = '\033[4m'
        # inverse = '\033[7m'
        # strike = '\033[9m'
        # colorama.ansi.AnsiStyle().ITALICS = 3
        # colorama.ansi.AnsiStyle().UNDERLINE = 4
        # colorama.ansi.AnsiStyle().INVERSE = 7
        # colorama.ansi.AnsiStyle().STRIKE = 9

        # example = colorama.Style
        # members = [attr for attr in dir(example) if not callable(getattr(example, attr)) and not attr.startswith("__")]
        # for x in members:
        #     log.debug(x)

    # def test1(self):
    #     test = {letter: f'{index:02d}' for index, letter in enumerate(string.ascii_lowercase, start=1)}
    #     pass
