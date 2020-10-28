from core.logger import log, json
from core import utils
import importlib
import os


class Initialize():
    def __init__(self):
        self.threads = []
        self.load()

    def load(self):
        mods = []
        for x in utils.util.scan('__init__.py'):
            mod = importlib.import_module(x, utils.util.abspath())
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
                    log.error(exc)
        log.debug('Manager has loaded all extensions')
