from core import logger


class patch():
    def __init__(self):
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
