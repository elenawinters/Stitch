from core.color import trace
from core import logger
import traceback
import random
import sys
import re
import os


class Utils:
    def __init__(self):
        pass

    class Enums:
        def __init__(self, enum):
            self.enum = enum

        def find(self, fetch):
            fetch = str(fetch).lower()
            for x in self.enum.__members__.items():
                if fetch == str(x[1].value) or fetch == str(x[1]) or fetch == str(x[0]):
                    return x[1]
            return self.enum.default  # Only meant to beused with enums that have a default entry. if no default entry, an error will be thrown.

    class Traceback:
        def __init__(self, exc):
            self.exc = exc

        def formatted(self, etype, value, tb):
            lines = traceback.format_list(traceback.extract_tb(tb))

            def shorten(match):
                return 'File "{}"'.format(os.path.basename(match.group(1)))
            lines = [re.sub(r'File "([^"]+)"', shorten, line, 1) for line in lines]
            try:
                return 'Traceback (most recent call last):\n' + ''.join(lines) + f'{etype.__name__}: {value}'
            except Exception:
                return 'Traceback (most recent call last):\n' + ''.join(lines) + f'{etype}: {value}'
            # Taken from https://stackoverflow.com/a/37059072

        def code(self):
            random.seed(self.formatted(*sys.exc_info()))
            number = random.randint(10000, 99999)
            return {'msg': f'Code #{number}', 'exc_info': self.exc}

        def trace(self):
            return [x for x in sys.exc_info()]

        def short(self):
            err = self.trace()
            return f"{err[0].__name__}: {err[1]}"

    def crypt(self, s):
        x = []
        for i in range(len(s)):
            j = ord(s[i])
            if 33 <= j <= 126:
                x.append(chr(33 + ((j + 14) % 94)))
            else:
                x.append(s[i])
        return ''.join(x)

    def excepthook(self, exctype, value, tb):
        logger.log.exception(**self.Traceback((exctype, value, tb)).code())

    def split(self, string, remove, offset=0):
        return string[len(f'{remove}') + offset:]

    def items(self, r, s):
        return [v for x in r for k, v in x.items() if k == s]

    def remove_duplicates(self, x: list):
        return list(dict.fromkeys(x))

    def search(self, find, data):
        return [x for x in data if find.lower() in str(x).lower()]

    def convert(self, text):
        return ''.join(i for i in text if ord(i) < 128)

    def remove(self, text):
        for x in trace.tracers:
            text = text.replace(str(x), '')
        return text

    def clean(self, text):  # Shorthand for self.convert and self.remove
        return self.convert(self.remove(text))

    def path(self, files):
        return os.path.join(os.path.dirname(os.path.abspath(files)))

    def abspath(self):
        return os.path.abspath('')

    def imports(self, fpath, folder):  # Get specific subfolder
        path = os.path.join(fpath, folder)
        return [self.split(os.path.join(root, name), self.abspath(), 1).replace('\\', '.')[:-3]
                for root, dirs, files in os.walk(path) for name in files
                if name.endswith('.py') and not name.endswith('__init__.py')]

    def scan(self, _file):  # Scan entire workspace for files
        return [self.split(os.path.join(root, name), self.abspath(), 1).replace('\\', '.')[:-3]
                for root, dirs, files in os.walk(self.abspath()) for name in files
                if name.endswith(_file)]


utils = Utils()
util = Utils()
