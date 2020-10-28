# from core.queue import queue
from core.logger import log
from core.utils import util
from dateutil import parser
from core import web, json
import threading
import time
import sys


# https://stackoverflow.com/a/3467879/14125122
class Initialize():  # Runtime debug
    def __init__(self):
        # for run in util.hack_the_planet():
        #     run(self)
        funcs = util.hack_the_planet()
        [threading.Thread(target=funcs[x], args=(self,), daemon=True, name=f'Debug-{x+1}').start() for x in range(len(funcs))]

    # def z_exit(self):  # If this is uncommented, it kills the program after all debug functions have run
    #     sys.exit(0)

    def tests(self):
        log.debug('Nothing to test!')

    def test1(self):
        log.debug(threading.current_thread().ident)
        # print(q.get())
        # self.queue.task_done()
        # queue.send('Debug.debug', 'what')
        # queue.send('Debug.debug', 'are')
        # queue.send('Debug.debug', 'you')
        # queue.send('Debug.debug', 'looking')
        # queue.send('Debug.debug', 'at', 9)
        # queue.send('Debug-6.debug', 'at', 9)

        # queue().append('test')
        # log.debug(queue.q())
        # {
        #     'from': threading.current_thread().getName(),
        #     'to': 'API.cache',
        #     'request': {
        #         'platform': 'discord',
        #         'type': 'prefix',
        #         'id': message.guild.id
        #     }
        # }
        # )

    # def test2(self):
    #     if item := queue.listen():
    #         log.debug(item)
        # log.debug(queue.listen(5))

        # time.sleep(5)
        # queue.listen()
        # time.sleep(2)
        # log.debug(queue.q())
        # pass

    # def test3(self):
    #     time.sleep(7)
    #     if item := queue.listen():
    #         log.debug(item)

    # def test4(self):
    #     time.sleep(7)
    #     if item := queue.listen():
    #         log.debug(item)

    # def test5(self):
    #     if item := queue.listen():
    #         log.debug(item)

    # def test6(self):
    #     if item := queue.listen():
    #         log.debug(item)

    # def test7(self):
    #     time.sleep(12)
    #     log.debug(queue.queue)
