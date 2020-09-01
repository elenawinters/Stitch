
class Utils:
    def __init__(self):
        pass

    def crypt(self, s):
        x = []
        for i in range(len(s)):
            j = ord(s[i])
            if 33 <= j <= 126:
                x.append(chr(33 + ((j + 14) % 94)))
            else:
                x.append(s[i])
        return ''.join(x)

    def split(self, string, remove, offset=0):
        return string[len(f'{remove}') + offset:]

    def search(self, find, data):
        return [x for x in data if find.lower() in str(x).lower()]


util = Utils()
