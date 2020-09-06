from core.color import trace
from core.logger import log
from core.utils import util
import subprocess
import threading
import inspect
import types
import time
import sys
import ast
import re


class Initialize():
    def __init__(self):
        threads = [threading.Thread(target=self.run, daemon=True, name='Updates')]
        [thread.start() for thread in threads]
        self.threads = []  # This thread will die eventually so we don't want to return that it may be alive

    def run(self):
        for name, run in inspect.getmembers(Initialize):  # Execute every function in this class
            if isinstance(run, types.FunctionType) and name not in [self.__init__.__name__, self.run.__name__]:
                try: run(self)
                except Exception as exc:
                    logger.log.exception(exc)

    def check_for_package_updates(self):
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

    def update_settings_file(self):  # Todo: update settings file if revision number does not match
        pass
