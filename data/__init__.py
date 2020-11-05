from core.logger import log, trace
from .data import data

priority = 1


class Initialize():
    def __init__(self):
        try:
            data.start()
            log.info(f'{trace.cyan}> Initialized {trace.black.s}dataset{trace.cyan} engine ({data.engine}).')
        except Exception as exc:
            log.warning(f'> Failed to load {trace.black.s}dataset{trace.warn}. Restarting!')
            log.exception(exc)
            sys.exit(0)
        self.response = None
