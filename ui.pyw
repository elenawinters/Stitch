"""
    This is a user interface wrapper for the Stitch framework.

    This emulates a console window, a command line interface,
    and allows for an overall easier operation.

    I hope I never have to touch this ever again after it's done.

"""

from core.color import trace
from core import logger, utils
import subprocess as sub
from tkinter import *
import tkinter as tk
import threading
import berry
from core import json
import asyncio
import time
import sys
import re
import os


# https://stackoverflow.com/a/47947223/14125122 (potential thread communication)
tkpattern = re.compile(r'.+?(?=\[|$)')
tkmatch = re.compile(r'\[.*?m')
name = json.orm['name']

# tracers = (styles.reset, styles.normal, styles.bold, styles.dim,
#                black, black.s, black.b, black.b.s,
#                red, red.s, red.b, red.b.s,
#                green, green.s, green.b, green.b.s,
#                yellow, yellow.s, yellow.b, yellow.b.s,
#                blue, blue.s, blue.b, blue.b.s,
#                magenta, magenta.s, magenta.b, magenta.b.s,
#                cyan, cyan.s, cyan.b, cyan.b.s,
#                white, white.s, white.b, white.b.s)
# https://github.com/elenawinters/Stitch/blob/870d5fd4932d06e9a9d69f4d70dee7b870fa3441/bots/discord/cogs/experiments/exp.py#L57
# http://www.science.smith.edu/dftwiki/images/3/3d/TkInterColorCharts.png
""" Convert colorama colors to tkinter colors. Use utils.util.match to get color. """
colvar = {
    (trace.black, trace.black.b): 'gray1', (trace.black.s, trace.black.b.s): '',
    (trace.red, trace.red.b): '', (trace.red.s, trace.red.b.s): '',
    (trace.green, trace.green.b): '', (trace.green.s, trace.green.b.s): '',
    (trace.yellow, trace.yellow.b): '', (trace.yellow.s, trace.yellow.b.s): 'yellow',
    (trace.blue, trace.blue.b): '', (trace.blue.s, trace.blue.b.s): '',
    (trace.magenta, trace.magenta.b): '', (trace.magenta.s, trace.magenta.b.s): '',
    (trace.cyan, trace.cyan.b): '', (trace.cyan.s, trace.cyan.b.s): '',
    (trace.white, trace.white.b): '', (trace.white.s, trace.white.b.s): ''
}

""" Tell the base color objects to load their string. """
colvar = {tuple([str(x) for x in k]): v for k, v in colvar.items()}
# [logger.log.debug(f'{k}: {v}') for k, v in colvar.items()]


class tkhandler(logger.logging.Handler):
    def __init__(self, widget):
        logger.logging.Handler.__init__(self)
        self.widget = widget

    def emit(self, record):
        # Append message (record) to the widget
        self.widget.insert(END, record.message + '\n')
        self.widget.see(END)


class tkfilter(logger.logging.Filter):
    def __init__(self, widget):
        self.widget = widget

    def filter(self, record):
        new_msg = []
        for match in re.findall(tkpattern, record.message):
            if color := re.match(tkmatch, match):
                col = utils.util.match(colvar, color.group())
                print(list(col.keys())[0])
                self.widget.tag_add('default', '5.0', '6.0')
        # col = [x for x in trace.tracers if x in record.message]
        # for x in trace.tracers:
        #     if x in record.message:
        #     print(x)
        return True


class stitches():
    def __init__(self):
        self.app = Tk()
        self.frame_left = Frame(self.app, width=200, height=400, bg='#6f7676')
        self.frame_right = Frame(self.app, width=650, height=400, bg='#6f7676')
        self.toolbar = Frame(self.frame_left, width=180, height=185, bg='#6f7676')

        self.console = Text(self.frame_right, bg="black", fg="white")
        self.console.pack(side='left', padx=5, pady=5)
        # self.console.grid(row=0, column=0, padx=5, pady=5)

        self.cscroll = Scrollbar(self.frame_right, orient="vertical", command=self.console.yview)
        self.cscroll.pack(side="right", expand=True, fill="y")

        self.console.configure(yscrollcommand=self.cscroll.set)
        # self.console.tag_configure('default', background='yellow')
        # self.console.tag_config()

        self.coords = Label(self.frame_left, text='Mouse Coordinates', relief=RAISED)
        self.coords.grid(row=99, column=0, padx=5, pady=5)

        self.color_config()

        self.console.bind('<Motion>', self.position)

        tkhand = tkhandler(self.console)
        tkhand.addFilter(tkfilter(self.console))
        logger.log.addHandler(tkhand)

    def test(self):
        t = self.console.tag_names(index=None)
        for x in t:
            logger.log.debug(x)

    def position(self, event):
        self.coords.config(text=f'XY: {event.x}, {event.y}')
        # Label(self.frame_left, text=f'XY: {event.x}, {event.y}', relief=RAISED).grid(row=99, column=0, padx=5, pady=5)

    def color_config(self):
        for k, v in colvar.items():
            if v:
                self.console.tag_configure(str(k), background=str(v))
            else:
                self.console.tag_configure(str(k), background='yellow')
        pass
        self.console.tag_configure('default', background='yellow')

    def run(self):
        self.app.title(name)
        self.app.geometry('850x450')
        # self.app.resizable(False, False)

        self.frame_left.grid(row=0, column=0, padx=10, pady=5)
        self.frame_right.grid(row=0, column=1, padx=10, pady=5)
        self.toolbar.grid(row=2, column=0, padx=5, pady=5)
        # self.frame_right.grid(row=0, column=1, padx=10, pady=5)
        # self.frame_right.pack(fill=BOTH, expand=YES)

        Label(self.frame_left, text=f'{name} User Interface', relief=RAISED).grid(row=0, column=0, padx=5, pady=5)

        # self.console.grid(row=0, column=0, padx=5, pady=5)
        # self.console.pack(expand=True, fill='both')

        Label(self.toolbar, text="General", relief=RAISED, fg="white", bg="#1a1a1a",).grid(row=0, column=0, padx=5, pady=3, ipadx=40)

        # self.start_button = Button(self.toolbar, text="Start", command=lambda: Thread(target=self.start_program).start()).grid(row=1, column=0, padx=5, pady=5, sticky='w' + 'e' + 'n' + 's')
        # Button(self.toolbar, text="Start", command=self.start_program).grid(row=1, column=0, padx=5, pady=5, sticky='w' + 'e' + 'n' + 's')
        Button(self.toolbar, text="Test", command=self.test).grid(row=2, column=0, padx=5, pady=5, sticky=W + E + N + S)
        Button(self.toolbar, text="Spam Console", command=self.test2).grid(row=3, column=0, padx=5, pady=5, sticky='w' + 'e' + 'n' + 's')

        self.app.configure(bg='#212121')

        threading.Thread(target=self.start_program, name=f'{name}UIWrapper', daemon=True).start()

        self.app.mainloop()

        return

    def test2(self):
        logger.log.debug('Spamming Console')
        for x in trace.tracers:
            logger.log.debug(f'{x}Hello world!')
        # for x in range(100):
        #     logger.log.debug(x)
        logger.log.debug('Console has been spammed')

    def start_program(self):
        try:
            berry.start()
        except Exception as exc:
            logger.log.exception(exc)


if __name__ == "__main__":
    stitches().run()
