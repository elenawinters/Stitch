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
    def reader(cls, data_type: str, f=default):
        if test:
            print('JSON File Read')
        if external.exists(f):
            return internal.fetch(data_type, f)

        try:
            # raise Exception
            from .enums import ReturnType
            return ReturnType.error
        except ModuleNotFoundError:
            raise IndexError("JSON Reader came back with an unknown error. "
                             "This happens when JSON Internal Fetch doesn't return anything, "
                             "or when the input file does not exist.")

    @classmethod
    def update(cls, data_type: str, value, f=default):
        if test:
            print('JSON File Update')
        internal.append(file, data_type, value, internal.open(f))
        if f == default:
            json()  # Reload memory

    write = update

    class ORMFile(object):
        def __init__(self, f=default):
            return f

        def f(self):
            return dict(self)['f']

    class ORM(dict, ORMFile):
        def __init__(self, f=default):
            super(self.__class__, self).__init__(f=f)

        def __getitem__(self, key):
            if test:
                print('JSON ORM Load')

            if self.f() == default:
                self.__dict__ = mem
            else:
                self.__dict__ = external.loads(f=self.f())

            if key not in self.__dict__:
                self.__dict__[key] = {}
                external.write(self.__dict__, f=self.f())
                if self.f() == default:
                    json()  # Reload memory
            return self.__dict__[key]

        def __setitem__(self, key, value):
            if test:
                print('JSON ORM Write')

            if self.f() == default:
                self.__dict__ = mem
            else:
                self.__dict__ = external.loads(f=self.f())

            # t = self.__dict__[key]
            # t.update()
            # self.__dict__.update()
            self.__dict__[key] = value
            external.write(self.__dict__, f=self.f())
            if self.f() == default:
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
    def fetch(cls, data_type: str, f=default, data=None):
        if test:
            print('JSON Internal Fetch')
        if data is None:
            data = external.loads(f)
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
    def append(cls, f: str, data_type: str, value: str, data=None):
        if test:
            print('JSON Internal Append')
        if data is None:
            data = external.loads(f)
        args = [x for x in data]  # PARSE ARGUMENTS
        found = False
        for x in args:
            if data_type == x:
                data[data_type] = value
                found = True

        if found is False:
            dump = {data_type: value}
            data.update(dump)

        external.write(data, f)

        return data

    update = append
    open = fetch


class External:
    @classmethod
    def exists(cls, f: str = default):
        if test:
            print('JSON External Exists')
        import os
        return os.path.isfile(f)

    @classmethod
    def loads(cls, f: str = default):
        if test:
            print('JSON External Loads')
        import os
        import json
        try:
            with open(f) as json_file:
                data = json.load(json_file)

            try:  # Update to new format
                data = json.loads(data)
                External.write(data, f=f)
            except TypeError:
                pass  # Up to date

        except json.JSONDecodeError:
            data = {}
        return data

    @classmethod
    def write(cls, data, f: str = default, mode='w'):
        if test:
            print('JSON External Write')
        import json
        with open(f, mode) as json_file:
            json.dump(data, json_file, indent=4)


internal = Internal
external = External
Json = JSON
json = JSON
