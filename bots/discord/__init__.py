from discord.ext import commands
from core.logger import log, trace
from core.queue import queue
from .core.tools import tls
from data.data import data
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
        self.queue = queue()
        tokens = json.orm['discord']['tokens']
        self.threads = [threading.Thread(target=self.run, args=(tls.crypt(x),), daemon=True) for x in tokens]
        for x in range(len(self.threads)):
            self.threads[x].name = f'Discord-{x + 1}'
            self.threads[x].start()

    def run(self, token):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        client = commands.Bot(command_prefix=self.prefix)
        loader.Load(client).load()

        loop.run_until_complete(client.start(token))
        loop.close()

    def prefix(self, bot, message):  # Logging does not work in this class. Use print for debugging
        """
            This is treated as an on_message event. So, on message, we return the prefix requirements for it to be a command.
            It's not good to call the database on every message. This will be transferred to the API at some point.
        """  # https://stackoverflow.com/a/56797589/14125122
        # print(threading.current_thread().getName())
        # q = queue()
        # # print(q.get())
        # # self.queue.task_done()
        # q.put(
        #     {
        #         'from': threading.current_thread().getName(),
        #         'to': 'API.cache',
        #         'request': {
        #             'platform': 'discord',
        #             'type': 'prefix',
        #             'id': message.guild.id
        #         }
        #     }
        # )

        # print(q.get())
        # print(q.get())
        # q.task_done()

        _pre = data.base['cache'].find_one(platform='discord', type='prefix', id=message.guild.id)
        if None:
            return json.orm['discord']['prefixes']['default']
        else:
            return _pre['data']
