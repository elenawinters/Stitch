"""
    Set custom variables for this class by following this example: https://stackoverflow.com/a/8307639/14125122

    Use queue.__class__ to get the class object and use setattr(class_object, variable, value)

    For example, "setattr(queue, mod, 0)" sets the variable mod of class queue (the class below) to 0

    This could theoretically be set to a class to allow for further setattr action

"""

from core.logger import log
from core import util
import threading
import inspect
import fity3
import time


class Queue:
    def __init__(self):
        if not hasattr(self, 'queue'):
            self.queue = []
            self.seen = []

    def assign(self, queue):  # Override
        if not isinstance(queue, type(None)):
            self.queue = queue
            self.seen = []

    def snowflake(self):
        return next(fity3.generator(0))

    def ident(self):
        thread = threading.current_thread().getName().split('-')[0]
        loc = inspect.stack()[2][1].split('\\')[-1].split('.')[0]
        return (thread + '.' + loc).lower()

    def send(self, receiver, message, expire=30):
        ident = self.ident()
        rec = receiver.lower()
        if ident == rec: return
        _dict = {
            'id': self.snowflake(),
            'sender': ident,
            'receiver': rec,
            'message': message,
            'expire': time.time() + expire
        }
        self.queue.append(_dict)
        return _dict

    def mark(self, id):
        self.seen.append(tuple([threading.current_thread().ident, id]))

    def verify(self, id):
        return (tuple([threading.current_thread().ident, id]) in self.seen)

    def listen(self, expire=None, rate=20):
        # log.debug(self.ident())
        """
            Set expiration if you need to have this in your own loops.
            Setting to 0 will cause it to exit loop as soon as it can.

            This needs to be optimized.
        """
        start = time.time()
        while True:  # <- This will likely cause issues.
            for x in range(len(q := self.queue)):
                if q[x]['expire'] < time.time():
                    self.seen = [y for y in self.seen if y[1] != q[x]['id']]
                    del self.queue[x]
                    break

                if q[x]['receiver'] == self.ident():
                    if self.verify(q[x]['id']):
                        continue
                    self.mark(q[x]['id'])
                    return q[x]

                if not isinstance(expire, type(None)) and (expire + start) < time.time():
                    return None

            time.sleep(1 / rate)  # Rate is 1 second divided by times per second


queue = Queue()
