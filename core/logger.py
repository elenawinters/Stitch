from core.color import trace
from core import json
from core import util
import core.defaults
import core.time
import logging
import enum
import sys


class LogLevel(enum.Enum):
    none = logging.NOTSET  # 0
    debug = logging.DEBUG  # 10
    info = logging.INFO  # 20
    warn = logging.WARN  # 30
    error = logging.ERROR  # 40
    critical = logging.CRITICAL  # 50
    default = info  # 20
    notset = none  # 0


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
            record.thrcol = trace.cyan

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
level = getattr(LogLevel, settings['level'], 'debug').value
log = logging.getLogger('stitches')
log.setLevel(logging.DEBUG)  # Void

stream_formatter = logging.Formatter('%(time)s [%(thrcol)s%(threadName)s%(reset)s] %(color)s%(message)s%(end)s')
stream = logging.StreamHandler(sys.stdout)
stream.setFormatter(stream_formatter)
stream.addFilter(StreamRecords())
stream.setLevel(level)
log.addHandler(stream)

file_formatter = logging.Formatter('[%(levelno)s] [%(name)s] [%(threadName)s] [%(module)s] [%(asctime)s] %(clean_msg)s')
files = logging.FileHandler(settings['name'], mode=settings['mode'])
files.setFormatter(file_formatter)
files.addFilter(FileRecords())
files.setLevel(level)
log.addHandler(files)

levels = LogLevel  # Alias for LogLevel
