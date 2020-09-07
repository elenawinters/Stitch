from core import logger, web, json
from core.utils import util
from dateutil import parser
import inspect
import types
import sys


# https://stackoverflow.com/a/3467879/14125122
class Initialize():  # Runtime debug
    def __init__(self):
        for run in util.hack_the_planet():
            logger.log.debug(f'Executing {__name__} function {run.__name__}')
            try: run(self)
            except Exception as exc:
                logger.log.exception(exc)
        # [run(self) for run in util.hack_the_planet()]
        # for name, run in inspect.getmembers(self.__class__):
        #     if isinstance(run, types.FunctionType) and name != self.__init__.__name__:
        #         logger.log.debug(f'Executing {__name__} function {name}')
        #         try: run(self)
        #         except Exception as exc:
        #             logger.log.exception(exc)

    # def z_exit(self):  # If this is uncommented, it kills the program after all debug functions have run
    #     sys.exit(0)

    def tests(self):
        logger.log.debug(logger.level.debug.value)

    def _r(self):
        logger.log.debug('test?')
