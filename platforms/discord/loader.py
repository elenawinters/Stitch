from core.bot.funcs import extensions
from core.color import trace
from core.logger import log
import core.utils
import os
custom_help = True


class Load:
    def __init__(self, client):
        self.client = client

    def load(self, silent=False):
        if custom_help:
            self.client.remove_command('help')
        cog_count = 0
        warnings = []
        cogs = self.extensions()
        for extension in cogs:
            try:
                self.client.load_extension(extension)
                cog_count += 1
            except Exception as e:
                if not silent:
                    warnings.append(f'Failed to load extension {extension}\n{e}')

        if not silent:
            if not cogs:
                log.warn('No extensions were found.')
            else:
                for x in warnings:
                    y = x.split('\n')
                    log.warning(f'> {y[0]}')
                    log.error(f'> {y[1]}')
                if len(warnings) > 0:
                    # if saved() < enums.LogLevel.error.value:
                    if len(warnings) == 1:
                        log.error(f'> Failed to load {trace.yellow.s}{len(warnings)}{trace.cyan} extension.')
                    else:
                        log.error(f'> Failed to load {trace.yellow.s}{len(warnings)}{trace.cyan} extensions.')
                log.info(f'{trace.cyan}> Loaded {trace.yellow.s}{cog_count}{trace.cyan} extensions!')

    def reload(self):
        pass

    def extensions(self):  # This works?
        abspath = os.path.abspath('')
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cogs')
        imports = [core.utils.util.split(os.path.join(root, name), f'{abspath}', 1).replace('\\', '.')[:-3]
                   for root, dirs, files in os.walk(f'{path}') for name in files
                   if name.endswith('.py') and not name.endswith('__init__.py')]
        return imports
