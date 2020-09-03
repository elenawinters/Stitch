# General information and static data storage.
from enum import Enum, auto


class Discord:
    class Avatars:  # Discord
        default = 'https://cdn.discordapp.com/embed/avatars/0.png'
        grey = 'https://cdn.discordapp.com/embed/avatars/1.png'
        green = 'https://cdn.discordapp.com/embed/avatars/2.png'
        yellow = 'https://cdn.discordapp.com/embed/avatars/3.png'
        red = 'https://cdn.discordapp.com/embed/avatars/4.png'
        blurple = default
        blue = default
        zero = default
        one = grey
        two = green
        three = yellow
        four = red
    error = 'https://www.mediafire.com/convkey/e259/b3pnjzoktk8vcszzg.jpg'
    default = error

    class Emotes:
        red_circle = 'http://www.mediafire.com/convkey/c36d/el585pkua4ff6i8zg.jpg'
        check = 'http://www.mediafire.com/convkey/92fc/mrsv5k8fs35e2ekzg.jpg'

    progress = {
        0: 'https://www.mediafire.com/convkey/a18d/5bnas7m3l9mpjyx6g.jpg',
        15: 'https://www.mediafire.com/convkey/bcca/hz7jlui2u6gq2ml6g.jpg',
        30: 'https://www.mediafire.com/convkey/f2f0/n1bw6tmaj6tb8vt6g.jpg',
        45: 'https://www.mediafire.com/convkey/05ea/u81bldz978zv2jn6g.jpg',
        60: 'https://www.mediafire.com/convkey/5a25/tqhighas2434c696g.jpg',
        75: 'https://www.mediafire.com/convkey/40ab/cf0349n2n99u1ec6g.jpg',
        90: 'https://www.mediafire.com/convkey/abd7/djpv9tuft5q891q6g.jpg',
        105: 'https://www.mediafire.com/convkey/bdf9/5qa6v106i84f5fi6g.jpg',
        120: 'https://www.mediafire.com/convkey/2ac0/3j9uvvzt979cyuz6g.jpg'
    }

    emotes = Emotes


class Images:
    class Coins:
        class Quarter:
            heads = 'https://www.mediafire.com/convkey/e737/0w5u9efs03xo5gxzg.jpg'
            tails = 'https://www.mediafire.com/convkey/43a4/tcrxt39knsguqm6zg.jpg'
    error = Discord.error
    default = error


class Game:
    type = {
        0: 'Playing',
        1: 'Streaming',
        2: 'Listening to',
        3: 'Watching'
    }
