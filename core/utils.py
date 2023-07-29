"""
    I always forget what these are meant to do.

    We can't import our logger here due to circular import.

"""

from typing import Any
from core.common.color import trace
import traceback
import inspect
import logging
import random
import string
import types
import sys
import re
import os

log = logging.getLogger('stitches')


class Utils:
    def __init__(self):
        pass

    class Enums:
        def __init__(self, enum):
            self.enum = enum

        def find(self, item, default='default'):
            return getattr(self.enum, item, default)

    class Traceback:
        def __init__(self, exc: Exception = None):
            self.exc = exc if not None else sys.exc_info()

        def formatted(self, tb):  # dont worry about converting this back. it's too difficult and we can seed this just fine
            new_frames = []
            for x in traceback.extract_tb(tb):
                frame = list(x)
                frame[0] = frame[0].replace(util.abspath(), '.')
                new_frames.append(tuple(frame))
            return new_frames

        def code(self):
            random.seed(str(self.formatted(self.exc.__traceback__)))
            number = random.randint(10000, 99999)  # i have no clue how useful these codes will actually be
            return {'msg': f'Error! Code #{number}', 'exc_info': self.exc}

    def excepthook(self, exctype, value, tb):
        return
        # log.error(**self.Traceback(value).code())
        # log.error("Uncaught exception: {0}".format(str(value)))
        # # print('here')
        # try:
        #     log.debug('here')
        #     log.error(**self.Traceback(sys.exc_info()).code())
        # except Exception as exc:
        #     print(exc)
        # print('finsihed')

    def crypt(self, s: str):
        x = []
        for i in range(len(s)):
            j = ord(s[i])
            if 33 <= j <= 126:
                x.append(chr(33 + ((j + 14) % 94)))
            else:
                x.append(s[i])
        return ''.join(x)

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

    class Types:  # saw this in an mCoding video. Useful for attempt() I think.
        NoReturn = object()

    async def attempt(self, func, *args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception:
            return util.Types.NoReturn

    def attempt(self, func, *args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception:
            return util.Types.NoReturn

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

    def split(self, string: str, remove: str, offset: int = 0):
        return string[len(f'{remove}') + offset:]

    def items(self, r, s):
        return [v for x in r for k, v in x.items() if k == s]

    def remove_duplicates(self, x: list):
        return list(dict.fromkeys(x))

    def search(self, find: str, data):
        return [x for x in data if find.lower() in str(x).lower()]

    def convert(self, text: str):
        return ''.join(i for i in text if ord(i) < 128)

    def remove(self, text: str):
        for x in trace.tracers:
            text = text.replace(str(x), '')
        return text

    def clean(self, text: str):  # Shorthand for self.convert and self.remove
        return self.convert(self.remove(text))

    def path(self, files):
        return os.path.join(os.path.dirname(os.path.abspath(files)))

    def abspath(self):
        return os.path.abspath('')

    def imports(self, fpath, folder='', ext='.py'):  # Get specific subfolder
        path = os.path.join(fpath, folder)
        return [self.split(os.path.join(root, name), self.abspath(), 1).replace('\\', '.')[:-len(ext)]
                for root, _, files in os.walk(path) for name in files
                if name.endswith(ext) and not name.endswith(f'__init__.py')]

    def scan(self, _file):  # Scan entire workspace for files
        return [self.split(os.path.join(root, name), self.abspath(), 1).replace('\\', '.')[:-3]
                for root, _, files in os.walk(self.abspath()) for name in files
                if name.endswith(_file)]


utils = Utils()
util = Utils()
utl = Utils()
