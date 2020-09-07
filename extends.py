from core import logger
from core import utils
import threading
import inspect
import types
import sys


# https://stackoverflow.com/a/3467879/14125122
class Initialize():  # Execute all functions in this class. Cannot be inherited from.
    def __init__(self):  # Probably bad practice, but I don't care.
        for run in utils.util.hack_the_planet():
            try: run(self)
            except Exception as exc:
                logger.log.exception(exc)
        logger.log.debug('Application extended')

    # def exception_hook(self):  # VS Code doesn't like exception hooks. This gets disabled in testing
    #     threading.excepthook = utils.util.excepthook
    #     sys.excepthook = utils.util.excepthook

    def asyncio_override(self):
        class asyncfilter(logger.logging.Filter):
            def filter(self, record):  # Appends prefix
                record.threadName = 'Asyncio'
                return True
        asynclog = logger.logging.getLogger('asyncio')
        asynclog.setLevel(logger.LogLevel.debug.value)
        asynclog.handlers = []  # Remove all handlers
        asynclog.addFilter(asyncfilter())
        asynclog.addHandler(logger.stream)
        asynclog.addHandler(logger.files)

    def flask_override(self):  # Aka werkzeug
        class flaskfilter(logger.logging.Filter):
            def filter(self, record):  # This shifts info to debug
                if record.levelno <= logger.LogLevel.info.value:
                    record.levelno = logger.LogLevel.debug.value
                record.threadName = 'Werkzeug'
                return True
        flasklog = logger.logging.getLogger('werkzeug')
        flasklog.setLevel(logger.LogLevel.debug.value)
        flasklog.handlers = []  # Remove all handlers
        flasklog.addFilter(flaskfilter())
        flasklog.addHandler(logger.stream)
        flasklog.addHandler(logger.files)

    def discord_override(self):
        discolog = logger.logging.getLogger('discord')
        discolog.setLevel(logger.LogLevel.info.value)
        discolog.addHandler(logger.stream)
        discolog.addHandler(logger.files)
