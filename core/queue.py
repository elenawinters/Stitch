from core.logger import log
from core.utils import util
import threading
import inspect
import time


class Queue:
    def __init__(self):
        if not hasattr(self, 'queue'):
            self.queue = []
            self.seen = []

    def assign(self, queue):  # Override
        if not isinstance(queue, type(None)):
            self.queue = queue

    def ident(self):
        thread = threading.current_thread().getName().split('-')[0]
        loc = inspect.stack()[2][1].split('\\')[-1].split('.')[0]
        return (thread + '.' + loc).lower()

    def send(self, receiver, message, expire=5):
        self.queue.append({
            'id': time.time_ns(),
            'sender': self.ident(),
            'receiver': receiver.lower(),
            'message': message,
            'expire': time.time() + expire
        })

    def mark(self, id):
        self.seen.append(tuple(threading.current_thread().ident, id))

    def verify(self, id):
        return (tuple(threading.current_thread().ident, id) in self.seen)

    def listen(self, expire=None):
        start = time.time()
        while True:
            for x in range(len(q := self.queue)):
                if q[x]['expire'] < time.time():
                    for y in range(len(s := self.seen)):
                        if y[s][1] == q[x]['id']:
                            del self.seen[s]
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
