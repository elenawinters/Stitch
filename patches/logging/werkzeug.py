from core import logger, json, utils


class patch():
    def __init__(self):
        class flaskfilter(logger.logging.Filter):
            def filter(self, record):  # This shifts info to debug
                record.threadName = 'Werkzeug'

                if record.levelno <= logger.LogLevel.info.value:
                    record.levelno = logger.LogLevel.debug.value

                return True

        flasklog = logger.logging.getLogger('werkzeug')
        flasklog.setLevel(logger.level)  # This needs to match the core logger, otherwise it will log using it's default
        flasklog.handlers = []  # Remove all handlers
        flasklog.addFilter(flaskfilter())
        flasklog.addHandler(logger.stream)
        flasklog.addHandler(logger.files)
