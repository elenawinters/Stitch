from core import logger, web, json
from core.utils import util
from dateutil import parser
import sys


# https://stackoverflow.com/a/3467879/14125122
class Initialize():  # Runtime debug
    def __init__(self):
        for run in util.hack_the_planet():
            logger.log.debug(f'Executing {__name__} function {run.__name__}')
            try: run(self)
            except Exception as exc:
                logger.log.exception(exc)

    # def z_exit(self):  # If this is uncommented, it kills the program after all debug functions have run
    #     sys.exit(0)

    def tests(self):
        logger.log.debug("Nothing to test")
