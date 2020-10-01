from discord.ext import commands
from core.logger import log, trace
from .core.tools import tls
import threading
import asyncio
from core import json
import subprocess
from . import loader
import time
import sys
import ast
import re


class Initialize():
    def __init__(self):
        tokens = json.orm['discord']['tokens']
        self.threads = [threading.Thread(target=self.run, args=(tls.crypt(x),), daemon=True) for x in tokens]
        for x in range(len(self.threads)):
            self.threads[x].name = f'Discord-{x + 1}'
            self.threads[x].start()

    def run(self, token):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        client = commands.Bot(command_prefix=self.prefix())
        loader.Load(client).load()

        loop.run_until_complete(client.start(token))
        loop.close()

    def prefix(self):
        # Todo: Implement https://stackoverflow.com/a/56797589/14125122
        return json.orm['discord']['prefixes']['default']
