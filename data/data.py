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


class Initialize():
    def __init__(self):
        log.info(f'{trace.cyan}> Initializing {trace.black.s}dataset{trace.cyan} Database.')
        try:
            data().start()
            log.info(f'{trace.cyan}> Initialized {trace.black.s}dataset{trace.cyan} engine ({data.engine}).')
            # log.info(f'{trace.cyan}> Initialized {trace.black.s}dataset{trace.cyan}. Engine: {tracer.yellow.s}{}')
        except Exception as err:
            log.exception(err)
            log.warning(f'> Failed to load {trace.black.s}dataset{trace.warn}. Restarting!')
            # log.error(f'> {short_traceback()}')
            # log.critical(f'> {traceback.format_exc()}')
            sys.exit(0)


class data:
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
        return cls.engine

    @classmethod
    def base(cls):
        return cls.base


class create:  # Create database/tables if not existant
    pass
