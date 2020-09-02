from core.logger import log, trace
from .core.tools import tls
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

        count = len(self.exc) - len(self.client.extensions)
        if count == 1: log.error(f'> Failed to load {trace.yellow.s}{count}{trace.cyan} extension.')
        else: log.error(f'> Failed to load {trace.yellow.s}{count}{trace.cyan} extensions.')
        log.info(f'{trace.cyan}> Loaded {trace.yellow.s}{len(self.client.extensions)}{trace.cyan} extensions!')

        # def out(t, x):
        #     log.warning(f'Failed to load extension {x}')
        #     log.error(t[x])

        # try:
        #     [out(x, t) for x in t]
        # except Exception as exc:
        #     log.exception(exc)

        # count = len(warnings) - len(self.client.extensions)
        # if count == 1: log.error(f'> Failed to load {trace.yellow.s}{count}{trace.cyan} extension.')
        # else: log.error(f'> Failed to load {trace.yellow.s}{count}{trace.cyan} extensions.')
        # log.info(f'{trace.cyan}> Loaded {trace.yellow.s}{len(self.client.extensions)}{trace.cyan} extensions!')

        # for x in cogs
        # for x in range(len(cogs)):
        #     try:
        #         self.client.load_extension(cogs[x])
        #     except Exception as e:
        #         log.warning(f'Failed to load extension {cogs[x]}')
        #         log.error(e)

        # warnings = len(cogs) - len(self.client.extensions)
        # if len(warnings) == 1:
        #     log.error(f'> Failed to load {trace.yellow.s}{len(warnings)}{trace.cyan} extension.')
        # else:
        #     log.error(f'> Failed to load {trace.yellow.s}{len(warnings)}{trace.cyan} extensions.')
        # log.error(f'> Failed to load {trace.yellow.s}{len(warnings)}{trace.cyan} extension.')
        # log.debug(len(self.client.extensions))
        # for x in self.client.extensions:
        #     log.debug(x)

        # if not silent:
        #     if not cogs:
        #         log.warn('No extensions were found.')
        #     else:
        #         for x in warnings:
        #             y = x.split('\n')
        #             log.warning(f'> {y[0]}')
        #             log.error(f'> {y[1]}')
        #         if len(warnings) > 0:
        #             # if saved() < enums.LogLevel.error.value:
        #             if len(warnings) == 1:
        #                 log.error(f'> Failed to load {trace.yellow.s}{len(warnings)}{trace.cyan} extension.')
        #             else:
        #                 log.error(f'> Failed to load {trace.yellow.s}{len(warnings)}{trace.cyan} extensions.')
        #         log.info(f'{trace.cyan}> Loaded {trace.yellow.s}{cog_count}{trace.cyan} extensions!')

    def reload(self):
        pass

    def restart(self):
        pass
