from core.logger import log, trace, json
import collections
import dataset
import sys
import os

'''
    dataset uses SQLAlchemy as a base.
    As such, our engine arguments need to conform to SQLAlchemy
    https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls

    Default engine is SQLite

'''


class data:
    def __new__(cls):  # This is disgusting
        cls.start(cls)

    @classmethod
    def start(cls):
        jdb = json.orm['settings']['database']
        if jdb['address'] == '/':  # Assuming SQLite, get default location
            jdb['address'] = '/' + str(os.path.abspath('data\\data.sqlite'))
            json.orm['settings'] = {'database': jdb}  # Merge updates

        db = dataset.connect(f"{jdb['engine']}://{jdb['address']}", engine_kwargs={'pool_recycle': 3600})
        cls.engine = jdb['engine']
        cls.base = db

    @classmethod
    def engine(cls):
        log.debug(cls.engine)
        return cls.engine

    @classmethod
    def base(cls):
        return cls.base


class create:  # Create database/tables if not existant
    pass
