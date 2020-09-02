from core import logger
import inspect
import types
import sys


# https://stackoverflow.com/a/3467879/14125122
class Initialize():  # Runtime debug
    def __init__(self):
        for name, run in inspect.getmembers(Initialize):
            if isinstance(run, types.FunctionType) and name != self.__init__.__name__:
                run(self)
        # logger.log.debug('Debug extension loaded')

    # def test_remove(self):
    #     from core.color import trace
    #     from core.utils import utils
    #     logger.log.debug(utils.remove(f'{trace.tracers} testing {trace.tracers}'))
