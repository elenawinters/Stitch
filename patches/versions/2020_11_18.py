from core import json


"""
    Name of framework is now specified in settings file.

"""


class update():
    def __init__(self):
        json.orm['name'] = 'Stitch'

        json.orm['revision'] = '2020.11.18'


if __name__ == "__main__":
    update()
