from threading import Thread
from core.color import trace
from core.logger import log
import subprocess
import time
import sys
import ast
import re


class Initialize(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.name = 'Updates'
        # self.name = f'{trace.alert}Updates{trace.reset}'
        self.start()

    def run(self):
        log.warn(f'{trace.warn}Checking for updates. This may take a minute.')
        pipreqs = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '-o', '--format=json'])
        pipreqs = ast.literal_eval(pipreqs.decode("utf-8"))

        reqs = []
        with open("requirements.txt", "r") as req_file:
            for line in req_file:
                reqs.append(re.split('<|=|>|~|!', line.strip())[0])

        # I keep confusing upd with udp, help me.
        upd = [x for x in pipreqs for y in reqs if x['name'].lower() == y.lower()]
        log.warn(f"Found updates for '{len(upd)}' module(s).")
        for x in upd:
            log.warn(f"{trace.warn}{x['name'].capitalize()} v{x['latest_version']} is available (v{x['version']} installed).")
