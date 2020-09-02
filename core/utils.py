import traceback
import random
import sys
import re
import os


class Utils():
    def __init__(self):
        pass

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

    def crypt(self, s):
        x = []
        for i in range(len(s)):
            j = ord(s[i])
            if 33 <= j <= 126:
                x.append(chr(33 + ((j + 14) % 94)))
            else:
                x.append(s[i])
        return ''.join(x)

    def split(self, string, remove, offset=0):
        return string[len(f'{remove}') + offset:]

    def search(self, find, data):
        return [x for x in data if find.lower() in str(x).lower()]


util = Utils()
