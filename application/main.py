import application.updates.updates
import application.api
# from application import updates, api
from threading import Thread
from core.logger import log


class Main(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.name = 'Application'
        self.start()

    def run(self):
        application.updates.updates.Main()
        application.api.Main()
