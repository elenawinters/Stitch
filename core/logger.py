
from core.color import trace
from core.utils import util
from core import json
import core.defaults
import core.time
import logging
import enum
import sys
import colorama
colorama.init()


class LogLevel(enum.Enum):
    none = logging.NOTSET  # 0
    debug = logging.DEBUG  # 10
    info = logging.INFO  # 20
    warn = logging.WARN  # 30
    error = logging.ERROR  # 40
    critical = logging.CRITICAL  # 50
    default = info  # 20, required by tls.Enums to be set


class StreamRecords(logging.Filter):
    def filter(self, record):
        # Special cases for all of the different log levels after this
        # This is a huge mess and I hate everything about it
        record.time = f'{trace.reset}[{trace.time}{core.time.misc.Now.unix()}{trace.reset}]'
        record.end = f'{trace.reset}{trace.alert}'
        record.reset = f'{trace.reset}'

        record.thrcol = ''
        record.color = ''

        if record.levelno >= 40:  # If error/critical
            record.thrcol = trace.red.s
            record.color = trace.alert
        elif record.levelno >= 30:  # If warning
            record.thrcol = trace.red
            record.color = trace.warn
        elif record.levelno <= 10:
            record.thrcol = trace.blue

        return True


class FileRecords(logging.Filter):
    def filter(self, record):
        record.clean_msg = util.clean(record.message)
        return True


class Logger():  # Define internal functions
    class Initialize():
        def __init__(self):
            json.memory.load()
            if not json.external.exists():
                self.create()  # Create file

        def create(self):
            json.external.write(core.defaults.default.settings)
            json.json()
            token = input(f"[{core.time.misc.Now.unix()}] What is the main Discord bot's login token? ")
            json.orm['discord'] = {'tokens': util.crypt(token)}


Logger.Initialize()
settings = json.orm['settings']['logging']
log = logging.getLogger('stitches')
log.setLevel(logging.DEBUG)  # Void

stream_formatter = logging.Formatter('%(time)s [%(thrcol)s%(threadName)s%(reset)s] %(color)s%(message)s%(end)s')
stream = logging.StreamHandler(sys.stdout)
stream.setFormatter(stream_formatter)
stream.addFilter(StreamRecords())
stream.setLevel(util.Enums(LogLevel).find(settings['console']['level']).value)
log.addHandler(stream)

file_formatter = logging.Formatter('[%(levelno)s] [%(name)s] [%(threadName)s] [%(module)s] [%(asctime)s] %(clean_msg)s')
files = logging.FileHandler(settings['file']['name'], mode=settings['file']['mode'])
files.setFormatter(file_formatter)
files.addFilter(FileRecords())
files.setLevel(util.Enums(LogLevel).find(settings['file']['level']).value)
log.addHandler(files)
