from core.logger import log
from core.utils import util
import importlib

priority = 0


class Initialize():
    def __init__(self):
        patches = util.imports(util.path(__file__))
        num = 0
        for x in patches:
            try:
                _patch = importlib.import_module(x, util.abspath())

                if hasattr(_patch, 'patch'):
                    patch = _patch.patch()

                    if hasattr(patch, 'response'):
                        if not isinstance(patch.response, type(None)):
                            log.debug(patch.response)
                    else:
                        log.debug(f"Patching {x.split('.')[-1]}")
                    num += 1
            except Exception as exc:
                log.exception(exc)

        self.response = f'Completed {num} patches'
