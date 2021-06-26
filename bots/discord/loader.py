from core.logger import log, trace
from discord.ext import commands
from .core.tools import tls
import threading
import time
import os


class CogLoader:
    def __init__(self, client):
        self.client = client
        self.exc = {}

    def load(self):
        self.client.remove_command('help')
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


class StitchEntryLoad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        old_name = threading.current_thread().name
        new_name = f'({old_name}) {self.bot.user.name}'
        threading.current_thread().name = new_name  # new thread name
        log.debug(f'Thread "{old_name}" changed name to "{new_name}"')
        log.debug(f'{self.bot.user.name} is ready! Loading extensions!')
        CogLoader(self.bot).load()


def setup(bot):
    bot.add_cog(StitchEntryLoad(bot))
