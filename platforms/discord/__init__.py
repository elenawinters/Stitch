from threading import Thread
from core.color import trace
from core.logger import log
import asyncio
import core.utils
from core import json
import subprocess
from . import loader
import core.utils
import discord
import time
import sys
import ast
import re


class Initialize(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.name = 'DiscordManager'
        self.start()

    def run(self):
        self.login()

    def login(self):
        def login_threads(token):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            client = discord.ext.commands.Bot(command_prefix=self.prefix())
            t = loader.Load(client).extensions()
            # log.debug(t)
            loader.Load(client).load()

            loop.run_until_complete(client.start(token))
            loop.close()
        tokens = json.json.orm['discord']['tokens']
        threads = [Thread(target=login_threads, args=(core.utils.util.crypt(x),), daemon=True) for x in tokens]
        t_count = 0
        for t in threads:
            t_count += 1
            t.name = f'Discord-{t_count}'
            t.start()

    def prefix(self):
        # Todo: Implement https://stackoverflow.com/a/56797589/14125122
        return json.json.orm['discord']['prefixes']['default']
