from discord.ext import commands
from core.logger import log, trace
from core.queue import queue
from .core.tools import tls
from data.data import data
import concurrent
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

        client = commands.Bot(command_prefix=self.prefix)
        loader.Load(client).load()

        loop.run_until_complete(client.start(token))
        loop.close()

    async def prefix(self, bot, message):  # Logging does not work in this class. Use print for debugging
        """
            This is treated as an on_message event. So, on message, we return the prefix requirements for it to be a command.
            It's not good to call the database on every message. This will be transferred to the API at some point.
        """  # https://stackoverflow.com/a/56797589/14125122

        # queue.send('api.__init__', ['discord', message.guild.id])
        # _pre = queue.listen(30)
        # log.debug(_pre)
        # return _pre['message']

        loop = asyncio.get_running_loop()

        def fetch():
            threading.current_thread().name = 'DiscordPrefix'
            queue.send('api.__init__', ['discord', message.guild.id])
            _pre = queue.listen(30)
            if _pre: return _pre['message']
            else: return None
            # self._prefix = _pre['message']

        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, fetch)

        return result

        # asyncio.run_coroutine_threadsafe(fetch(), bot.loop)

        # t = bot.loop.run_until_complete(asyncio.gather(fetch()))

        # fut = asyncio.run_coroutine_threadsafe(fetch(), self.loop)
        # t = fut.result(5)
        # log.debug(f'prefix?')

        # return '.'

        # t = asyncio.run_coroutine_threadsafe(asyncio.gather(fetch()), self.loop)
        # # t = self.loop.run_until_complete(asyncio.gather(fetch()))
        # log.debug(f'future {t}')
        # t = asyncio.run_coroutine_threadsafe(fetch(), self.loop)
        # log.debug(f'future {t}')

        # return '.'

        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.run_until_complete(asyncio.ensure_future(fetch()))

        # asyncio.get_running_loop().run_until_complete(asyncio.ensure_future(fetch()))
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

        # _pre = data.base['cache'].find_one(platform='discord', type='prefix', id=message.guild.id)
        # if None:
        #     return json.orm['discord']['prefixes']['default']
        # else:
        #     return _pre['data']
