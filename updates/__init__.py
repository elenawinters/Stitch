from core.color import trace
from core.logger import log
from core.utils import util
import subprocess
import threading
import time
import sys
import ast
import re


class Initialize():  # Yes, I'm addicted to list comprehensions - EW
    def __init__(self):  # Run every function in this class on a different thread
        funcs = util.hack_the_planet()
        [threading.Thread(target=funcs[x], args=(self,), daemon=True, name=f'Updates-{x+1}').start() for x in range(len(funcs))]

    def check_for_package_updates(self):
        log.warn(f'{trace.warn}Checking for updates. This may take a minute.')
        pipreqs = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '-o', '--format=json'])
        pipreqs = ast.literal_eval(pipreqs.decode("utf-8"))

        reqs = []
        with open("requirements.txt", "r") as req_file:
            [reqs.append(re.split('<|=|>|~|!', line.strip())[0]) for line in req_file]

        upd = [x for x in pipreqs for y in reqs if x['name'].lower() == y.lower()]
        log.warn(f"Found updates for '{len(upd)}' module(s).")
        [log.warn(f"{trace.warn}{x['name'].capitalize()} v{x['latest_version']} is available (v{x['version']} installed).") for x in upd]
