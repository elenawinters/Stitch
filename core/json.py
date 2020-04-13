# Do not use TLS log functions
# in this class. Everything
# will reset and break.
# Central to Login sequence
protected = ['token', 'secure']
default = 'settings.json'
test = False
mem = {}


class JSON:
    def __init__(self):
        global mem
        mem = external.loads()
        try:
            from core.logger import log
            log.debug('> JSON Memory Refreshed.')
        except ModuleNotFoundError:
            pass
        except ImportError:
            pass

    @classmethod
    def reader(cls, data_type: str, file=default):
        if test:
            print('JSON File Read')
        if external.exists(file):
            return internal.fetch(data_type, file)

        try:
            # raise Exception
            from .enums import ReturnType
            return ReturnType.error
        except ModuleNotFoundError:
            raise IndexError("JSON Reader came back with an unknown error. "
                             "This happens when JSON Internal Fetch doesn't return anything, "
                             "or when the input file does not exist.")

    @classmethod
    def update(cls, data_type: str, value, file=default):
        if test:
            print('JSON File Update')
        internal.append(file, data_type, value, internal.open(file))
        json()  # Reload memory

    write = update

    class ORM(dict):
        def __getitem__(self, key):
            if test:
                print('JSON ORM Load')
            self.__dict__ = mem
            if key not in self.__dict__:
                self.__dict__[key] = {}
                external.write(self.__dict__)
                json()  # Reload memory
            return self.__dict__[key]

        def __setitem__(self, key, value):
            if test:
                print('JSON ORM Write')
            self.__dict__ = mem
            self.__dict__[key] = value
            external.write(self.__dict__)
            json()  # Reload memory

    orm = ORM()

    # The JSON ORM is still a work in progress (WIP)
    # Most issues will revolve around actually setting values using the ORM.
    # The ORM allows for very complicated usage. Using the ORM is preferred.


class Internal:  # Underlying functions for JSON
    @classmethod  # JSON -> Dict
    def loads(cls, data):
        if test:
            print('JSON Internal Loads')
        import json
        literal = json.loads(data)
        return literal

    @classmethod  # Dict -> JSON
    def dumps(cls, data):
        if test:
            print('JSON Internal Dumps')
        import json
        literal = json.dumps(data)
        return literal

    @classmethod
    def fetch(cls, data_type: str, file=default, data=None):
        if test:
            print('JSON Internal Fetch')
        if data is None:
            data = external.loads(file)
        if data is not None:
            args = [x for x in data]  # PARSE ARGUMENTS
            for x in args:
                if data_type == x:
                    return data[x]
        try:
            from .enums import ReturnType
            return ReturnType.none
        except ModuleNotFoundError:
            return None

    @classmethod
    def append(cls, file: str, data_type: str, value: str, data=None):
        if test:
            print('JSON Internal Append')
        if data is None:
            data = external.loads(file)
        args = [x for x in data]  # PARSE ARGUMENTS
        found = False
        for x in args:
            if data_type == x:
                data[data_type] = value
                found = True

        if found is False:
            dump = {data_type: value}
            data.update(dump)

        external.write(data, file)

        return data

    update = append
    open = fetch


class External:
    @classmethod
    def exists(cls, file: str = default):
        if test:
            print('JSON External Exists')
        import os
        return os.path.isfile(file)

    @classmethod
    def loads(cls, file: str = default):
        if test:
            print('JSON External Loads')
        import os
        import json
        with open(file) as json_file:
            data = json.loads(json.load(json_file))
        return data

    @classmethod
    def write(cls, data, file: str = default, mode='w'):
        if test:
            print('JSON External Write')
        import json
        with open(file, mode) as json_file:
            json.dump(json.dumps(data), json_file)


internal = Internal
external = External
Json = JSON
json = JSON





