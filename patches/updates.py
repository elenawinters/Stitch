from core.color import trace
from core.logger import log
from core.utils import util
import subprocess
import threading
import importlib
import string
import time
import sys
import ast
import re


letters = {l: i for i, l in enumerate(string.ascii_lowercase, start=1)}
versions = [x for x in util.imports(util.path(__file__), '', '.pyw')]


def numeric(i):
    s = i.split('.')[-3:]
    if (l := list(''.join(s))[-1]) in letters:
        s.append(letters[l])
    else:
        s.append(letters['a'])

    num = ''.join(f'{int(x):02d}' for x in s)
    return num


class patch():
    def __init__(self):
        [run(self) for run in util.hack_the_planet()]
        self.response = None

    def check_for_package_updates(self):
        def in_thread():
            log.warn(f'{trace.warn}Checking for updates. This may take a minute.')
            pipreqs = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '-o', '--format=json'])
            pipreqs = ast.literal_eval(pipreqs.decode("utf-8"))

            with open("requirements.txt", "r") as req_file:
                reqs = [re.split('<|=|>|~|!', line.strip())[0] for line in req_file]

            upd = [x for x in pipreqs for y in reqs if x['name'].lower() == y.lower()]
            log.warn(f"Found updates for '{len(upd)}' module(s).")
            [log.warn(f"{trace.warn}{x['name'].capitalize()} v{x['latest_version']} is available (v{x['version']} installed).") for x in upd]

        threading.Thread(target=in_thread, daemon=True, name='Updates').start()

    def update_resources(self):
        versions.sort(key=numeric, reverse=True)

        log.debug(versions)
