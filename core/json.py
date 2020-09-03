from core.defaults.default import default
import json as _json
import collections
import datetime
import os


class memory:
    @classmethod
    def load(cls, files=default):
        cls.exists(files)
        if files not in cls.memory.keys():
            cls.memory[files] = {}
            return cls.reload(files)
        return cls.memory[files]

    @classmethod
    def reload(cls, files=default):  # Yuck
        cls.exists(files)
        internal.merge(cls.memory[files], external.loads(files=files))
        return cls.memory

    @classmethod
    def refresh(cls, files=default):
        cls.reload(files)

    @classmethod
    def exists(cls, files=default):
        try: cls.memory
        except Exception:
            cls.memory = {}


class ORMFile(object):  # Why does this fucking work?
    def __init__(self, files=default):
        return files

    def files(self):
        return dict(self)['files']


class ORM(dict, ORMFile):  # This is a huge mess
    def __init__(self, files=default):
        super(self.__class__, self).__init__(files=files)

    def __getitem__(self, key):
        files = self.files()
        self.__dict__[files] = memory.load(files)

        if key not in self.__dict__[files]:
            self.__dict__[files][key] = {}
            external.write(self.__dict__[files], files=files)
            memory.reload(files)

        return self.__dict__[files][key]

    def __setitem__(self, key, value):
        self.update(self, key, value)

    def update(self, key, value):
        files = self.files()
        self.__dict__[files] = memory.load(files)

        # self.__dict__[key] = value
        internal.merge(self.__dict__[files], {key: value})
        external.write(self.__dict__[files], files=files)
        memory.reload()


orm = ORM()


# Eg: https://gist.github.com/simonw/7000493
class Encode(_json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class Decode(_json.JSONDecoder):
    pass


encode = Encode()
decode = Decode()


class Internal:
    @classmethod
    def merge(cls, dct, merge_dct):  # https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
        for k, v in merge_dct.items():
            if (k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], collections.Mapping)):
                cls.merge(dct[k], merge_dct[k])
            else:
                dct[k] = merge_dct[k]
        return dct

    @classmethod
    def loads(cls, data):
        return _json.loads(data)

    @classmethod
    def dumps(cls, data, pretty=False):
        if pretty: return _json.dumps(data, indent=2, separators=(", ", ": "), default=str)
        else: return _json.dumps(data)


class External:
    @classmethod
    def exists(cls, files: str = default):
        return os.path.isfile(files)

    @classmethod
    def loads(cls, files: str = default):
        try:
            with open(files) as json_file:
                data = _json.load(json_file)

            try:  # Update to new format
                data = _json.loads(data)
                cls.write(data, files=files)
            except TypeError:
                pass  # Up to date

        except _json.JSONDecodeError:
            data = {}
        return data

    @classmethod
    def write(cls, data, files: str = default, mode='w'):
        with open(files, mode) as json_file:
            _json.dump(data, json_file, indent=4)


internal = Internal
external = External
