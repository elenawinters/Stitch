from core import logger, web, json
from dateutil import parser
import inspect
import types
import sys


# https://stackoverflow.com/a/3467879/14125122
class Initialize():  # Runtime debug
    def __init__(self):
        for name, run in inspect.getmembers(Initialize):
            if isinstance(run, types.FunctionType) and name != self.__init__.__name__:
                logger.log.debug(f'Executing {__name__} function {name}')
                try: run(self)
                except Exception as exc:
                    logger.log.exception(exc)

    # def z_exit(self):  # If this is uncommented, it kills the program after all debug functions have run
    #     sys.exit(0)

    def tests(self):
        json.memory.loads(['test.json', 'test2.json', 'extreme_test.json', 'rerere.json'])
        t = json.memory.internal()
        json.external.write(t, 'test_dump.json')
        # logger.log.debug(json.memory.internal())

        # r = json.ORM('settings.json')
        # json.ORM('test.json')
        # logger.log.debug(t)
        # host = json.orm['api']  # Post current time to api
        # uptime = web.Client(f"http://{host['host']}:{host['port']}/uptime/").get()
        # logger.log.debug(uptime.json()['uptime'])
