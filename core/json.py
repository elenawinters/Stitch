# THIS IS GOING TO BE DEPRECIATED
# CONFIGPARSER WILL REPLACE IT

# https://codebeautify.org/json-generator
from core.defaults.default import default
import json as _json
try:
    from collections.abc import Mapping
except ImportError:  # backwards compat
    from collections import Mapping
import datetime
import os


class memory:
    @classmethod
    def merge(cls, file: str):
        internal.merge(cls.memory[file], external.loads(file=file))

    @classmethod
    def loads(cls, files: list[str] = [default]):
        for file in files:
            cls.load(file)

    @classmethod
    def load(cls, file: str = default):
        cls.exists()
        if file not in cls.memory.keys():
            cls.memory[file] = {}
            cls.merge(file)
        return cls.memory[file]

    @classmethod
    def reloads(cls):
        for x in cls.memory.keys():
            cls.reload(x)

    @classmethod
    def reload(cls, file: str = default):  # Yuck
        cls.exists()
        cls.merge(file)
        return cls.memory

    @classmethod
    def update(cls, file: str = default):
        cls.exists()
        cls.memory[file] = {}
        cls.merge(file)

    @classmethod
    def refresh(cls, file: str = default):
        cls.reload(file)

    @classmethod
    def internal(cls):
        return cls.memory

    @classmethod
    def exists(cls):
        try: cls.memory
        except Exception:
            cls.memory = {}


class ORMFile(object):  # Why does this fucking work?
    def __init__(self, file: str = default):
        return file

    def file(self):
        return dict(self)['file']


class ORM(dict, ORMFile):  # This is a huge mess
    def __init__(self, file: str = default):
        super().__init__(file=file)

    def __getitem__(self, key: str):
        file = self.file()
        self.__dict__[file] = memory.load(file)

        if key not in self.__dict__[file]:
            self.__dict__[file][key] = {}
            external.write(self.__dict__[file], file=file)
            memory.reload(file)

        return self.__dict__[file][key]

    def __setitem__(self, key: str, value: str):
        self.update(key, value)

    def update(self, key: str, value: str):
        file = self.file()
        self.__dict__[file] = memory.load(file)

        # self.__dict__[key] = value
        internal.merge(self.__dict__[file], {key: value})
        external.write(self.__dict__[file], file=file)
        memory.reload()


orm = ORM()


# Eg: https://gist.github.com/simonw/7000493
class Encode(_json.JSONEncoder):  # This isn't used
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class Decode(_json.JSONDecoder):
    pass


encode = Encode()
decode = Decode()


class Internal:
    @classmethod
    def merge(cls, dct: dict, merge_dct: dict):  # https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
        for k, v in merge_dct.items():
            if (k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], Mapping)):
                cls.merge(dct[k], merge_dct[k])
            else:
                dct[k] = merge_dct[k]
        return dct

    @classmethod
    def loads(cls, data: str):
        return _json.loads(data)

    @classmethod
    def dumps(cls, data: dict, pretty: bool = False):
        if pretty: return _json.dumps(data, indent=2, separators=(", ", ": "), default=str)
        else: return _json.dumps(data)


class External:
    @classmethod
    def exists(cls, file: str = default):
        return os.path.isfile(file)

    @classmethod
    def loads(cls, file: str = default):
        if cls.exists(file):
            with open(file) as json_file:
                data = _json.load(json_file)
            return data
        return {}  # File does not exist.

    @classmethod
    def write(cls, data: dict, file: str = default, mode: str = 'w'):
        with open(file, mode) as json_file:
            _json.dump(data, json_file, indent=4)


internal = Internal
external = External
