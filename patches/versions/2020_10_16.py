from core.logger import log
import os


"""
    This is only here because this is the start of local updates.

    Anything below this version is unsupported (mainly cuz the defaults file was actually wrong).

"""


class update():
    def __init__(self):
        log.debug(f'Unable to update to {os.path.basename(__file__)}')
