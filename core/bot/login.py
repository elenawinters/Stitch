import discord
from core.color import *
# from .funcs import *
from .tools import *
from core.logger import log
from core.bot import enums
from core import json
import traceback
import requests
import loader
import sys
import os
from threading import Thread
import asyncio
loop = None


class LoginManager:
    def __init__(self, prefix):
        self.prefix = prefix

    def login(self):
        log.info(f'{trace.cyan}> Attempting Login.')
        log.info(f'{trace.cyan}> Running on {trace.white}Discord{trace.green.s}Py '
                 f'{trace.cyan}v{trace.cyan.s}{discord.__version__}{trace.cyan}.')
        tokens = json.json.orm['tokens']
        for x in tokens:
            client = commands.Bot(command_prefix=self.prefix)
            LoginMultiple(client, crypt(x))
        return


class LoginMultiple(Thread):
    def __init__(self, client, token=None):
        Thread.__init__(self)
        self.client = client
        self.token = token
        self.daemon = True
        self.start()

    def run(self):
        global loop
        try:
            if loop:
                loader.Load(self.client).run(silent=True)
                loop.create_task(_login(self.client, self.token))
            else:
                loop = self.client.loop
                loader.Load(self.client).run()
                loop.create_task(_login(self.client, self.token))
                loop.run_forever()
        except Exception as exc:
            log.exception(exc)

        return


async def _login(client, token=None):
    if not token:
        try:
            log.info(f'{trace.cyan}> Attempting Login.')
            log.info(f'{trace.cyan}> Running on {trace.white}Discord{trace.green.s}Py '
                     f'{trace.cyan}v{trace.cyan.s}{discord.__version__}{trace.cyan}.')
            version.Discord.latest()
            version.YouTubeDL.latest()
            token = json.json.reader('token')
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
            except:
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
            except:
                pass

    @classmethod
    def parse(cls, late: list, curr: list):
        if late == curr:
            return False
        return True




