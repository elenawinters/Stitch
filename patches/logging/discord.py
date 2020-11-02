from core import logger


class patch():
    def __init__(self):
        discolog = logger.logging.getLogger('discord')
        discolog.setLevel(logger.LogLevel.info.value)
        discolog.addHandler(logger.stream)
        discolog.addHandler(logger.files)
