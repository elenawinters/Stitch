
class queue:
    def __new__(self, queue=None):
        if not isinstance(queue, type(None)):
            print('this should run once')
            self.queue = queue

        if hasattr(self, 'queue'):
            return self.queue
