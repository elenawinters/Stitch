from twitchio.ext import commands
# from discord.ext import commands
import twitchio

from core import utils, assets
import traceback
import colorsys
import datetime
import random
import httpx
import sys
import re
import os


class TwitchTools(utils.Utils):
    def __init__(cls):  # inherit core.utils
        super().__init__()


tls = TwitchTools()  # Define tls
