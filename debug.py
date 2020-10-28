from core import logger, web, json
from core.queue import queue
from core.utils import util
from dateutil import parser
import threading
import sys


# https://stackoverflow.com/a/3467879/14125122
class Initialize():  # Runtime debug
    def __init__(self):
        funcs = util.hack_the_planet()
        # for x in funcs:
        #     print(x)
        [threading.Thread(target=funcs[x], args=(self,), daemon=True, name=f'Debug-{x+1}').start() for x in range(len(funcs))]
        # for run in util.hack_the_planet():
        #     logger.log.debug(f'Executing {__name__} function {run.__name__}')
        #     try: run(self)
        #     except Exception as exc:
        #         logger.log.exception(exc)

    # def z_exit(self):  # If this is uncommented, it kills the program after all debug functions have run
    #     sys.exit(0)

    def tests(self):
        logger.log.debug('Nothing to test!')

    # def test1(self):
    #     print('test1')
    #     # print(q.get())
    #     # self.queue.task_done()
    #     queue().append('test')
    #     print(queue()[0])
    #     # {
    #     #     'from': threading.current_thread().getName(),
    #     #     'to': 'API.cache',
    #     #     'request': {
    #     #         'platform': 'discord',
    #     #         'type': 'prefix',
    #     #         'id': message.guild.id
    #     #     }
    #     # }
    #     # )

    # def test2(self):
    #     print('test2')
    #     print(queue()[0])
    #     pass

    # def test3(self):
    #     print('test3')
    #     pass
