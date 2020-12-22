import discord
from discord.ext import commands
from core.logger import log, trace
# from core.queue import queue
from .core.tools import tls
from data.data import data
from core import web
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

        intents = discord.Intents.default()
        intents.presences = True
        intents.members = True

        client = commands.Bot(command_prefix=self.prefix, intents=intents)
        loader.Load(client).load()

        loop.run_until_complete(client.start(token))
        loop.close()

    def prefix(self, bot, message):
        """
            This is treated as an on_message event. So, on message, we return the prefix requirements for it to be a command.
        """  # https://stackoverflow.com/a/56797589/14125122

        _pre = data.base['cache'].find_one(platform='discord', type='prefix', id=message.guild.id)
        if _pre: return _pre['data']
        else:
            return json.orm['discord']['prefixes']['default']
