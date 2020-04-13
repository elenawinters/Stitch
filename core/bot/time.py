from core.color import trace
import datetime


class Time:
    @classmethod
    def diff(cls, before: datetime.datetime, after: datetime.datetime):
        return after - before

    class Now:
        def __new__(cls):
            return str(datetime.datetime.utcnow())

        @classmethod
        def unix(cls):
            import time
            return time.strftime("%X", time.localtime(time.time()))
        logger = unix

    @classmethod
    def test(cls):
        import time
        return time.strftime("%X and %x", time.localtime(time.time()))

    class Parse:
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
                date = time.readable.date().replace(',', f'{color},{trace.time}')
                return f'{trace.time}{time.readable.time()}{color} on {trace.time}{date}{color}'
            else:
                return f'{time.readable.time()} on {time.readable.date()}'

        @classmethod
        def on(cls, color=trace.cyan):
            if color:
                date = time.readable.date().replace(',', f'{color},{trace.time}')
                return f'{trace.time}{date}{color} at {trace.time}{time.readable.time()}{color}'
            else:
                return f'{time.readable.date()} at {time.readable.time()}'

        @classmethod
        def date(cls):
            import time
            return time.strftime("%A, %B %d, %Y", time.localtime(time.time()))

        @classmethod
        def time(cls):
            import time
            return time.strftime("%r", time.localtime(time.time()))

        @classmethod
        def military(cls):
            import time
            return time.strftime("%R", time.localtime(time.time()))

        class From:
            class Timedelta:
                @classmethod
                def seconds(cls, r: datetime.timedelta):
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
                        if seconds > 0:
                            o.append(f'and {seconds} seconds')
                    else:
                        o.append(f'{seconds} seconds')
                    if len(o) > 2:
                        return ', '.join(o)
                    else:
                        return ' '.join(o)
                    # return f'{r.days} days, {hours} hours, {minutes} minutes, and {seconds} seconds'

                @classmethod
                def microseconds(cls, r: datetime.timedelta):
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
                        o.append(f'and {seconds}.{r.microseconds} seconds')
                    else:
                        o.append(f'{seconds}.{r.microseconds} seconds')
                    if len(o) > 2:
                        return ', '.join(o)
                    else:
                        return ' '.join(o)

            timedelta = Timedelta
    readable = Readable


time = Time
