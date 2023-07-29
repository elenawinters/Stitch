import discord
from discord.ext import commands
# from core.logger import log, trace
# from core.queue import queue
# from .core.tools import tls
from core.common import web
import concurrent
import threading
import asyncio
import subprocess
import time
import sys
import ast
import re
import os


# TODO: IF POSSIBLE, MOVE THIS TO __INIT__.PY. WE NEED TO REDO MANAGER

class Initialize():
    def __init__(self):
        # tokens = json.orm['discord']['tokens']
        self.threads = [threading.Thread(target=self.run, args=(tls.crypt(x),), daemon=True) for x in tokens]
        for x in range(len(self.threads)):
            self.threads[x].name = f'Discord-{x + 1}'
            self.threads[x].start()

    def run(self, token):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        intents = discord.Intents.default()
        intents.presences = True
        intents.members = True

        client = commands.Bot(command_prefix=self.prefix, intents=intents)
        entry_cog = tls.split(os.path.join(tls.path(__file__), 'main'), tls.abspath(), 1).replace('\\', '.')
        client.load_extension(entry_cog)
        # loader.Load(client).load()

        loop.run_until_complete(client.start(token))
        loop.close()