from core import json


"""
    A bug was discovered that causes logger errors.

    If the console log level is info, while the file log level
    is debug, record.message does not appear in file records.

    This merges console and file log settings to just a general setting.

"""


class update():
    def __init__(self):
        for k, v in json.orm['settings']['logging']['file'].items():
            json.orm['settings'] = {
                'logging': {
                    k: v
                }
            }

        js = json.external.loads()
        del js['settings']['logging']['console']
        del js['settings']['logging']['file']
        try:  # This field appears when the bug happens due to json handling
            del js['file']
        except Exception: pass
        json.external.write(js)
        json.memory.update()

        json.orm['revision'] = '2020.11.11'


if __name__ == "__main__":
    update()
