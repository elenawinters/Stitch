# import prompt_toolkit as prompt
from core.color import trace
from core.logger import log
from core.utils import util
import threading
import readline
import asyncio
import time
import sys
import ast
import io
import re


# https://stackoverflow.com/a/4653306/14125122
class Initialize():
    def __init__(self):
        raise Exception('not ready')
        # funcs = util.hack_the_planet()
        # self.threads = [threading.Thread(target=x, args=(self,), daemon=True, name=f'CLI') for x in funcs]
        self.threads = [threading.Thread(target=self.stitches, daemon=True, name='CLI')]
        [thread.start() for thread in self.threads]

    def stitches(self):
        while True:
            log.debug(input())
        # for line in sys.stdin:
        #     log.debug(line.replace('\n', ''))
