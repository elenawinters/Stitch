from core.logger import log, json
from core import util
import importlib
import sys
import os


class Initialize():
    def __init__(self):
        self.file = '__load__.py'
        self.threads = []
        self.load()

    def load(self):
        mods = []
        for x in util.scan(self.file):
            mod = importlib.import_module(x, util.abspath())
            # priortity = (2 - 2**-23) * 2**127
            priority = 9223372036854775807
            if hasattr(mod, 'priority'):
                priority = mod.priority

            mods.append({
                'priority': priority,
                'mod': mod,
                'loc': x
            })

        def advm(elem):
            return elem.get('priority')

        mods.sort(key=advm)

        for x in mods:
            if x.get('loc').split('.')[-2] not in json.orm['settings']['manager']['ignore']:
                try:
                    mod = x.get('mod').Initialize()

                    if hasattr(mod, 'threads'):
                        self.threads += mod.threads

                    if hasattr(mod, 'response'):
                        if not isinstance(mod.response, type(None)):
                            log.debug(mod.response)
                    else:
                        log.debug(f"Loaded {x.get('loc')[:-9]}")

                except Exception as exc:
                    log.exception(**util.Traceback(exc).code())
                    # log.error(util.Traceback(exc).formatted(*sys.exc_info()))

        log.debug('Manager has loaded all extensions')
