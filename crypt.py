# This is a standalone script to ROT47 incoming text

import json
import ast


def crypt(s):
    x = []
    for i in range(len(s)):
        j = ord(s[i])
        if 33 <= j <= 126:
            x.append(chr(33 + ((j + 14) % 94)))
        else:
            x.append(s[i])
    return ''.join(x)


if __name__ == "__main__":
    t = input('JSON Input?: ')
    t = json.dumps(crypt(t))
    print(type(t))
    print(t)
    x = input()
