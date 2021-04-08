from core.logger import log, trace
from .core.tools import tls
import time
import os


class Load:
    def __init__(self, client):
        # THIS IS FOR TWITCH. THIS NEEDS TO BE PATCHED UP TO WORK AS IT IS PORTED FROM DISCORD
        self.client = client
        self.exc = {}

    def load(self):
        # self.client.remove_command('help')
        self.reload()

    def reload(self):  # https://stackoverflow.com/a/42376244/14125122
        cogs = tls.remove_duplicates(tls.imports(tls.path(__file__), 'cogs'))
        loaded = [x for x in self.client.extensions]

        for x in cogs:
            try:
                if x in loaded:
                    self.client.reload_extension(x)
                    loaded.remove(x)
                else:
                    self.client.load_extension(x)
            except Exception as e: self.exc.update({x: e})

        for x in self.exc:
            log.warning(f'Failed to load extension {x}')
            log.error(self.exc[x])

        count = len(self.exc)
        if count == 1: log.error(f'> Failed to load {trace.yellow.s}{count}{trace.cyan} extension.')
        else: log.error(f'> Failed to load {trace.yellow.s}{count}{trace.cyan} extensions.')
        log.info(f'{trace.cyan}> Loaded {trace.yellow.s}{len(self.client.extensions)}{trace.cyan} extensions!')

    def restart(self):
        pass
