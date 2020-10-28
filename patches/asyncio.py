from core import logger


class patch():
    def __init__(self):
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
