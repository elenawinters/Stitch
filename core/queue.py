from core.logger import log
from core.utils import util
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

    def snowflake(self):
        return next(fity3.generator(0))

    def ident(self):
        thread = threading.current_thread().getName().split('-')[0]
        loc = inspect.stack()[2][1].split('\\')[-1].split('.')[0]
        return (thread + '.' + loc).lower()

    def send(self, receiver, message, expire=30):
        self.queue.append({
            'id': self.snowflake(),
            'sender': self.ident(),
            'receiver': receiver.lower(),
            'message': message,
            'expire': time.time() + expire
        })
        log.debug(self.queue[-1])

    def mark(self, id):
        self.seen.append(tuple([threading.current_thread().ident, id]))

    def verify(self, id):
        return (tuple([threading.current_thread().ident, id]) in self.seen)

    def listen(self, expire=None):
        start = time.time()
        while True:
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

                if expire and (expire + start) < time.time():
                    return None


queue = Queue()
