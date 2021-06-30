from core import logger


class patch():
    def __init__(self):
        class asyncfilter(logger.logging.Filter):
            def filter(self, record: logger.logging.LogRecord):
                record.threadName = 'Asyncio'

                """
                    Errors and above get shifted to none.
                    I can't find a way to catch an Asyncio error.

                    The error that usually occurs is ConnectionResetError.
                    It doesn't seem to have any adverse effects to normal function.

                    This error has been happening for months and I'm annoyed by it.

                """

                if record.levelno >= logger.LogLevel.error.value:
                    record.levelno = logger.LogLevel.none.value

                return True

        asynclog = logger.logging.getLogger('asyncio')
        asynclog.setLevel(logger.LogLevel.debug.value)
        asynclog.handlers = []  # Remove all handlers
        asynclog.addFilter(asyncfilter())
        asynclog.addHandler(logger.stream)
        asynclog.addHandler(logger.files)
