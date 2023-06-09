"""
    Written by Elena Winters.
    Copyright 2018-2023.

    I don't know when I initially created this file,
    but I made my bot in 2018, and this was an early addition.

    This is basically a wrapper around colorama.
    It makes it easier for me to program with it.

"""

from colorama import Fore, Back, Style
import colorama
colorama.init()

def __color_container(normal, normal_strong, background, background_strong):
    class __color_class:
        class B:
            s = background_strong

            def __str__(self):
                return background
        b = B()
        s = normal_strong
        def __str__(self):
            return normal
    return __color_class()


class Trace:
    """
    B stands for background
    S stands for strong

    """
    reset = Style.RESET_ALL
    normal = Style.NORMAL
    generic = Fore.CYAN
    name = Fore.LIGHTYELLOW_EX
    message = Fore.LIGHTGREEN_EX
    type = Fore.LIGHTMAGENTA_EX
    alert = Fore.LIGHTRED_EX
    warn = Fore.LIGHTYELLOW_EX
    id = Fore.LIGHTCYAN_EX
    time = Fore.LIGHTGREEN_EX

    class Styles:
        reset = Style.RESET_ALL
        normal = Style.NORMAL
        bold = Style.BRIGHT
        dim = Style.DIM
        bright = bold

    styles = Styles

    # 2023: Trying to make this nicer to look at instead of just duplicates of itself over and over for each color
    black = __color_container(Fore.BLACK, Fore.LIGHTBLACK_EX, Back.BLACK, Back.LIGHTBLACK_EX)
    red = __color_container(Fore.RED, Fore.LIGHTRED_EX, Back.RED, Back.LIGHTRED_EX)
    green = __color_container(Fore.GREEN, Fore.LIGHTGREEN_EX, Back.GREEN, Back.LIGHTGREEN_EX)
    yellow = __color_container(Fore.YELLOW, Fore.LIGHTYELLOW_EX, Back.YELLOW, Back.LIGHTYELLOW_EX)
    blue = __color_container(Fore.BLUE, Fore.LIGHTBLUE_EX, Back.BLUE, Back.LIGHTBLUE_EX)
    magenta = __color_container(Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Back.MAGENTA, Back.LIGHTMAGENTA_EX)
    cyan = __color_container(Fore.CYAN, Fore.LIGHTCYAN_EX, Back.CYAN, Back.LIGHTCYAN_EX)
    white = __color_container(Fore.WHITE, Fore.LIGHTWHITE_EX, Back.WHITE, Back.LIGHTWHITE_EX)

    # Tuple of all color objects implemented in this class. 36 objects in total.
    tracers = (styles.reset, styles.normal, styles.bold, styles.dim,

               black, black.s, black.b, black.b.s,
               red, red.s, red.b, red.b.s,
               green, green.s, green.b, green.b.s,
               yellow, yellow.s, yellow.b, yellow.b.s,
               blue, blue.s, blue.b, blue.b.s,
               magenta, magenta.s, magenta.b, magenta.b.s,
               cyan, cyan.s, cyan.b, cyan.b.s,
               white, white.s, white.b, white.b.s)

    @classmethod
    def clean(cls, text: str):  # removes all color codes and converts to ascii
        for x in cls.tracers:
            text = text.replace(str(x), '')
        return ''.join(i for i in text if ord(i) < 128)


trace = Trace
