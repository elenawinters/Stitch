from core.logger import log
from core import json
import os


class update():
    def __init__(self):
        log.debug(f'Unable to update to {os.path.basename(__file__)}')
        # for x in json.orm['discord']:
        #     log.debug('here')
