# Threading assistance provided by RingoMar
import discord
from core.color import *
# from .funcs import *
from .tools import *
from core.logger import log
from core.bot import enums
from core import json
import threading
import traceback
import httpx as requests
import loader
import sys
import os
import time
import asyncio


class LoginManager:
    def __init__(self, prefix):
        self.prefix = prefix

    def login(self):
        log.info(f'{trace.cyan}> Attempting Login.')
        log.info(f'{trace.cyan}> Running on {trace.white}Discord{trace.green.s}Py '
                 f'{trace.cyan}v{trace.cyan.s}{discord.__version__}{trace.cyan}.')
        version.Discord.latest()
        version.YouTubeDL.latest()
        tokens = json.json.orm['tokens']['discord']
        threads = [threading.Thread(target=login_threads, args=(self.prefix, crypt(x),), daemon=True) for x in tokens]
        # threads = [threading.Thread(target=login_threads, args=(self.prefix, crypt(x),)) for x in tokens]
        return threads


def login_threads(prefix, token=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = commands.Bot(command_prefix=prefix)
    loader.Load(client).run()

    loop.run_until_complete(_login(client, token))
    loop.close()


async def _login(client, token=None):
    if not token:
        try:
            log.info(f'{trace.cyan}> Attempting Login.')
            log.info(f'{trace.cyan}> Running on {trace.white}Discord{trace.green.s}Py '
                     f'{trace.cyan}v{trace.cyan.s}{discord.__version__}{trace.cyan}.')
            version.Discord.latest()
            version.YouTubeDL.latest()
            # token = json.json.reader('token')
            if token == enums.ReturnType.fail or token == enums.ReturnType.none:
                raise discord.errors.LoginFailure('No token')
            else:
                await client.start(crypt(token))
                # client.run(crypt(token))
                return
        except discord.errors.LoginFailure as e:
            if json.external.exists(json.default):
                try:
                    os.remove(json.default)
                except OSError:
                    pass
            log.critical(f'{type(e)} has occurred. Please check your login token')
            log.critical('SESSION HAS BEEN TERMINATED')
            log.critical(f'{e}')
        except Exception as err:  # This should never occur.
            log.error(f'> {short_traceback()}')
            log.error(f'> {traceback.format_exc()}')
    else:
        await client.start(token)
        # client.run(token)
        return


class version:
    class Discord:
        @classmethod
        def latest(cls):
            try:  # Late for latest, curr for current.
                base = f"https://api.github.com/repos/Rapptz/discord.py/tags"
                info = requests.get(base).json()[0]['name']
                info = info.replace('v', '')
                # info = '1.2.9'
                late = info
                curr = discord.__version__.split('.')
                late = late.split('.')
                for x in range(len(curr)):
                    curr[x] = int(curr[x])
                for x in range(len(late)):
                    late[x] = int(late[x])

                new = version.parse(late, curr)
                if new:
                    log.warning(f'{trace.alert}> {trace.white}Discord{trace.green.s}Py {trace.cyan}v{trace.cyan.s}'
                                f'{info}{trace.green.s} is {trace.yellow.s}available{trace.cyan}.')
                    log.warning(f'{trace.alert}> {trace.yellow.s}Please update to {trace.cyan}v{trace.cyan.s}{info}{trace.cyan}.')
            except Exception:
                pass

    class YouTubeDL:
        @classmethod
        def latest(cls):
            try:  # Late for latest, curr for current.
                base = f"https://api.github.com/repos/ytdl-org/youtube-dl/tags"
                info = requests.get(base).json()[0]['name']
                # info = '2038.01.19'
                late = info
                import youtube_dl
                # curr = youtube_dl.options.__version__.split('.')
                curr = youtube_dl.options.__version__
                show = curr
                curr = curr.split('.')
                late = late.split('.')
                for x in range(len(curr)):
                    curr[x] = int(curr[x])
                for x in range(len(late)):
                    late[x] = int(late[x])

                new = version.parse(late, curr)
                if new:
                    log.warning(f'{trace.alert}> {trace.cyan}Running on {trace.white.b}{trace.black}You{trace.red.b.s}'
                                f'{trace.white.s}Tube{trace.reset}-{trace.red.s}DL {trace.cyan}v{trace.cyan.s}{show}{trace.cyan}.')
                    log.warning(f'{trace.alert}> {trace.yellow.s}Please update {trace.white.b}{trace.black}'
                                f'You{trace.red.b.s}{trace.white.s}Tube{trace.reset}-{trace.red.s}DL '
                                f'{trace.yellow.s}to {trace.cyan}v{trace.cyan.s}{info}{trace.cyan}.')
            except Exception:
                pass

    @classmethod
    def parse(cls, late: list, curr: list):
        if late == curr:
            return False
        return True
