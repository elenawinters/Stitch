from core.logger import log
from core import utils
import importlib
import os


class Initialize():
    def __init__(self):
        self.load()

    def path(self):
        return os.path.abspath('')

    def scan(self):  # Some dumb shit. I hate that I have to do it this way
        return [utils.Utils().split(os.path.join(root, name), self.path(), 1).replace('\\', '.')[:-3]
                for root, dirs, files in os.walk(self.path()) for name in files
                if name.endswith("__init__.py")]

    def load(self):
        for x in self.scan():
            try:
                importlib.import_module(x, self.path()).Initialize()
                log.debug(f'Loaded {x[:-9]}')
            except Exception as exc:
                log.error(exc)
