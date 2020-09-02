from core.logger import log
from core import utils
import importlib
import os


class Initialize():
    def __init__(self):
        self.threads = []
        self.load()

    def load(self):
        for x in utils.util.scan('__init__.py'):
            try:
                self.threads += importlib.import_module(x, utils.util.abspath()).Initialize().threads
                log.debug(f'Loaded {x[:-9]}')
            except Exception as exc:
                log.error(exc)
