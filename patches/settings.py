from core.logger import log
from core.utils import util
import importlib
import string


class patch():
    def __init__(self):
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

        versions.sort(key=numeric, reverse=True)

        log.debug(versions)
        # for x in versions
        self.response = None
