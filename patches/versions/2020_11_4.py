from core import json


"""
    This version changed how activity data is stored.

"""


class update():
    def __init__(self):
        for k, v in json.orm['discord']['activity'].items():
            json.orm['discord'] = {
                'presence': {
                    k: {
                        'status': 'online',
                        'activity': v
                    }
                }
            }

        js = json.external.loads()
        del js['discord']['activity']
        json.external.write(js)
        json.memory.update()

        json.orm['revision'] = '2020.11.4'


if __name__ == "__main__":
    update()
