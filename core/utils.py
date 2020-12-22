from core.color import trace
from core import logger
import traceback
import inspect
import random
import string
import types
import sys
import re
import os


class Utils:
    def __init__(self):
        pass

    class Enums:
        def __init__(self, enum):
            self.enum = enum

        def find(self, item, default='default'):
            return getattr(self.enum, item, default)

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

    class switch:  # https://stackoverflow.com/a/6606540/14125122
        def __init__(self, value):
            self.value = value
            self._entered = False
            self._broken = False
            self._prev = None

        def __enter__(self):
            return self

        def __exit__(self, type, value, traceback):
            return False  # Allows a traceback to occur

        def __call__(self, *values):
            if self._broken:
                return False

            if not self._entered:
                if values and self.value not in values:
                    return False
                self._entered, self._prev = True, values
                return True

            if self._prev is None:
                self._prev = values
                return True

            if self._prev != values:
                self._broken = True
                return False

            if self._prev == values:
                self._prev = None
                return False

        @property
        def default(self):
            return self()

    # class switch(object):  # https://stackoverflow.com/a/6606540/14125122
    #     def __init__(self, value):
    #         self.value = value
    #         self.fall = False

    #     def __iter__(self):
    #         """Return the match method once, then stop"""
    #         yield self.match
    #         raise StopIteration

    #     def match(self, *args):
    #         """Indicate whether or not to enter a case suite"""
    #         if self.fall or not args:
    #             return True
    #         elif self.value in args:
    #             self.fall = True
    #             return True
    #         else:
    #             return False

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

    def hack_the_planet(self, ignore: list = []):  # This is overly complicated.
        """ This returns every function from the class it was executed from """
        frame = inspect.stack()[1][0]
        ignores = [frame.f_code.co_name] + ignore
        funcs = []
        for name, run in inspect.getmembers(frame.f_locals['self'].__class__):
            if isinstance(run, types.FunctionType) or isinstance(run, types.MethodType):
                if name not in ignores and not name.startswith('__') and not name.endswith('__'):
                    funcs.append(run)
        return funcs

    def match(self, obj, key):
        """This is mainly meant for dicts with tuples as the key, to find the value"""
        for k, v in obj.items():
            if isinstance(k, str):
                if key == k:
                    return k, v
            else:
                # [return v, k for x in k if find == x]
                for x in k:
                    if key == x:
                        return k, v
        # print('no match')
        return  # We don't return anything

    def random_string(self, **kwargs):
        return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(kwargs.get('min', 1), kwargs.get('max', 25))))

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

    def imports(self, fpath, folder='', ext='.py'):  # Get specific subfolder
        path = os.path.join(fpath, folder)
        return [self.split(os.path.join(root, name), self.abspath(), 1).replace('\\', '.')[:-len(ext)]
                for root, dirs, files in os.walk(path) for name in files
                if name.endswith(ext) and not name.endswith(f'__init__.py')]

    def scan(self, _file):  # Scan entire workspace for files
        return [self.split(os.path.join(root, name), self.abspath(), 1).replace('\\', '.')[:-3]
                for root, dirs, files in os.walk(self.abspath()) for name in files
                if name.endswith(_file)]


utils = Utils()
util = Utils()
utl = Utils()
