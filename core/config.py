import configparser
import sys
import os


# THIS IS NOT FUNCTIONAL.
# When I get around to it, this will replace the JSON settings file.
class ConfigManager(configparser.ConfigParser):
    def __init__(self, file='config.ini'):
        sys.exit(0)
        self.config = super().__init__()
        self.file = file
        self.read()

    def read(self):
        if os.path.exists(self.file):
            self.config.read(self.file)

    def save(self):
        try:
            with open(self.file, 'w') as file:
                self.config.write(file)
        except Exception as exc:
            for _ in range(3):
                print(exc)

    def write(self):
        self.save()
