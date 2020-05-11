from core.defaults import setup
from core.bot.tools import tls
from core.bot.time import time
from core.color import trace
from core import json
import logging
import enum
import sys
import colorama
colorama.init()


class LogLevel(enum.Enum):
    debug = logging.DEBUG  # 10
    info = logging.INFO  # 20
    warn = logging.WARN  # 30
    error = logging.ERROR  # 40
    critical = logging.CRITICAL  # 50
    default = info  # 20, required by tls.Enums to be set


class StreamRecords(logging.Filter):
    def filter(self, record):
        # Special cases for all of the different log levels after this
        record.time = f'{trace.time}[{time.Now.unix()}]{trace.reset}'
        record.end = f'{trace.reset}{trace.alert}'

        if record.levelno >= 40:  # If error/critical
            record.color = trace.alert
        elif record.levelno >= 30:  # If warning
            record.color = trace.warn
        else:  # Regular/none
            record.color = ''

        return True


class FileRecords(logging.Filter):
    def filter(self, record):
        record.clean_msg = clean(record.message)
        return True


setup.startup()
settings = json.json.orm['settings']['logging']
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Void

stream_formatter = logging.Formatter('%(time)s [%(threadName)s] %(color)s%(message)s%(end)s')
stream = logging.StreamHandler(sys.stdout)
stream.setFormatter(stream_formatter)
stream.addFilter(StreamRecords())
stream.setLevel(tls.Enums(LogLevel).find(settings['console']['level']).value)
log.addHandler(stream)

file_formatter = logging.Formatter('[%(levelno)s] [%(name)s] [%(threadName)s] [%(module)s] [%(asctime)s] %(clean_msg)s')
file = logging.FileHandler(settings['file']['file'], mode='a+')
file.setFormatter(file_formatter)
file.addFilter(FileRecords())
file.setLevel(tls.Enums(LogLevel).find(settings['file']['level']).value)
log.addHandler(file)


def clean(text):  # Make writable to file
    for x in trace.tracers:
        text = text.replace(str(x), '')
    return ''.join(i for i in text if ord(i) < 128)
