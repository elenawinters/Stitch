# from data.data import get_data_file
from core.json import default
settings_file = default
settings = {
    'discord': {
        'prefix': '.',
        'tokens': [],
        'activity': {
            'default': {
                'name': 'games',
                'type': 0
            }
        }
    },
    'twitch': {
        'prefix': '!',
        'tokens': []
    },
    'api': {
        'host': '127.0.0.1',
        'port': 5000,
    },
    'external': {
        'youtube': None,
        'twitch': None
    },
    'settings': {
        'logging': {
            'console': {
                'level': 'default'
            },
            'file': {
                'level': 'default',
                'name': 'log.txt',
                'mode': 'a+'
            }
        },
        'database': {
            'engine': 'sqlite',
            'address': '/'
        }
    }
}
