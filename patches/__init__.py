from core.logger import log
from core.utils import util
import importlib

priority = 0


class Initialize():
    def __init__(self):
        patches = util.imports(util.path(__file__), '')
        for x in patches:
            log.debug(f"Patching {x.split('.')[-1]}")
            try:
                importlib.import_module(x, util.abspath()).patch()
            except Exception as exc:
                log.exception(exc)
        self.response = f'Completed {len(patches)} patches'
