from core.color import trace
import time as _time
import datetime


class Misc:
    @classmethod
    def uptime(cls, launched):
        return readable.timedelta(self.diff(launched, datetime.datetime.utcnow()))

    @classmethod
    def diff(cls, before: datetime.datetime, after: datetime.datetime):
        return after - before

    class Now:
        def __new__(cls):
            return str(datetime.datetime.utcnow())

        @classmethod
        def unix(cls):
            return _time.strftime("%X", _time.localtime(_time.time()))
        logger = unix

    @classmethod
    def test(cls):
        return _time.strftime("%X and %x", _time.localtime(_time.time()))


class Parse:  # This is meant primarily for the discord bot's .embed command
    @classmethod
    def iso(cls, string: str):  # ISO 8601 to datetime
        if 'Z' in string or 'T' in string:
            string = string.replace('T', ' ')
            string = string.replace('Z', '')
        return string


class Readable:
    @classmethod
    def at(cls, color=trace.cyan):
        if color:
            date = cls.date().replace(',', f'{color},{trace.time}')
            return f'{trace.time}{cls.time()}{color} on {trace.time}{date}{color}'
        else:
            return f'{cls.time()} on {cls.date()}'

    @classmethod
    def on(cls, color=trace.cyan):
        if color:
            date = cls.date().replace(',', f'{color},{trace.time}')
            return f'{trace.time}{date}{color} at {trace.time}{cls.time()}{color}'
        else:
            return f'{cls.date()} at {cls.time()}'

    @classmethod
    def date(cls):
        return _time.strftime("%A, %B %d, %Y", _time.localtime(_time.time()))

    @classmethod
    def time(cls):
        return _time.strftime("%r", _time.localtime(_time.time()))

    @classmethod
    def military(cls):
        return _time.strftime("%R", _time.localtime(_time.time()))

    class Timedelta:
        def __new__(cls, r: datetime.timedelta, micro=False):
            hours = r.seconds // 3600
            minutes = (r.seconds // 60) % 60
            seconds = r.seconds % 60

            o = []

            if r.days > 0:
                o.append(f'{r.days} days')
            if hours > 0:
                o.append(f'{hours} hours')
            if minutes > 0:
                o.append(f'{minutes} minutes')

            if len(o) > 0:
                if micro:  # Microseconds
                    o.append(f'and {seconds}.{r.microseconds} seconds')
                else:
                    if seconds > 0:
                        o.append(f'and {seconds} seconds')
            else:
                if micro:  # Microseconds
                    o.append(f'{seconds}.{r.microseconds} seconds')
                else:
                    o.append(f'{seconds} seconds')

            if len(o) > 2:
                return ', '.join(o)
            else:
                return ' '.join(o)

    timedelta = Timedelta


readable = Readable


misc = Misc
