from core.logger import log, trace
from .core.tools import tls
import time
import os


class Load:
    def __init__(self, client):
        self.client = client
        self.exc = {}

    # https://stackoverflow.com/a/42376244/14125122
    def load(self):
        self.client.remove_command('help')
        cogs = tls.remove_duplicates(tls.imports(tls.path(__file__), 'cogs'))

        for x in cogs:
            try: self.client.load_extension(x)
            except Exception as e: self.exc.update({x: e})

        for x in self.exc:
            log.warning(f'Failed to load extension {x}')
            log.error(self.exc[x])

        count = len(self.exc)
        if count == 1: log.error(f'> Failed to load {trace.yellow.s}{count}{trace.cyan} extension.')
        else: log.error(f'> Failed to load {trace.yellow.s}{count}{trace.cyan} extensions.')
        log.info(f'{trace.cyan}> Loaded {trace.yellow.s}{len(self.client.extensions)}{trace.cyan} extensions!')

    def reload(self):
        pass
        # before = time.monotonic()
        # cogs = tls.remove_duplicates(tls.imports(tls.path(__file__), 'cogs'))
        # loaded = [x for x in self.bot.extensions]
        # # search = [x for x in cogs if x in loaded]
        # for x in cogs: if x in loaded: try:
        #     self.client.reload_extension(x)
        #     loaded.remove(x)
        # except Exception as e:
        #     self.exc.update({x: e})
        # elif x not in loaded: try:
        #     self.bot.load_extension(x)
        #     loading.append(x)

        # for x in self.exc:
        #     log.warning(f'Failed to reload extension {x}')
        #     log.error(self.exc[x])

    def restart(self):
        pass
