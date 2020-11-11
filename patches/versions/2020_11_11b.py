from core import json


"""
    Add a support command (this is predefined here. Can be changed in the settings file)

"""


class update():
    def __init__(self):
        json.orm['discord'] = {
            'support': {
                'name': 'Stitch Support',
                'url': 'https://discord.gg/v7M8gT5'
            }
        }

        json.orm['revision'] = '2020.11.11b'


if __name__ == "__main__":
    update()
