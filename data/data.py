from core import json
import dataset


def get_data_file():
    import os
    abspath = os.path.abspath('.')
    if os.path.dirname(abspath) == 'data':
        path = abspath
    else:
        path = f'{abspath}\\data'
    return path


class Data:
    def __new__(cls):
        jdb = json.json.orm['settings']['database']
        if jdb['path'] is None:
            path = f"{get_data_file()}\\{jdb['file']}"
        else:
            path = f"{jdb['path']}\\{jdb['file']}"
        db = dataset.connect(f'sqlite:///{path}?check_same_thread=false', engine_kwargs={'pool_recycle': 3600})
        cls.base = db

    @classmethod
    def base(cls):
        return cls.base


data = Data
