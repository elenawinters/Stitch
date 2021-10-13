"""
    AMBITION REWRITE

    This will be seperated into multiple locations and such.
    Ambition rewrite will primarily be a UI application unless disabled.


    OLD STRING

    This is a user interface wrapper for the Stitch framework.

    This emulates a console window, a command line interface,
    and allows for an overall easier operation.

    I hope I never have to touch this ever again after it's done. -EW

"""

from dataclasses import dataclass
from core.color import trace
from core import logger, util
import subprocess as sub
from tkinter import *
import tkinter as tk
import threading
import berry
from core import json
import asyncio
import random
import time
import sys
import re
import os


@dataclass
class ScrollbarPosition:
    hi: int = 0
    lo: int = 0


# https://stackoverflow.com/a/47947223/14125122 (potential thread communication)
tkpattern = re.compile(r'.+?(?=\[|$)')
scroll_pos = ScrollbarPosition(0, 0)
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
    (trace.black, trace.black.b): 'black', (trace.black.s, trace.black.b.s): 'gray',
    (trace.red, trace.red.b): 'red3', (trace.red.s, trace.red.b.s): 'red',
    (trace.green, trace.green.b): 'dark green', (trace.green.s, trace.green.b.s): 'green',
    (trace.yellow, trace.yellow.b): 'gold', (trace.yellow.s, trace.yellow.b.s): 'yellow',
    (trace.blue, trace.blue.b): 'royal blue', (trace.blue.s, trace.blue.b.s): 'blue',
    (trace.magenta, trace.magenta.b): 'magenta3', (trace.magenta.s, trace.magenta.b.s): 'magenta',
    (trace.cyan, trace.cyan.b): 'cyan3', (trace.cyan.s, trace.cyan.b.s): 'cyan',
    (trace.white, trace.white.b): 'light grey', (trace.white.s, trace.white.b.s): 'white'
}

""" Tell the base color objects to load their string. """
colvar = {tuple([str(x) for x in k]): v for k, v in colvar.items()}
# [logger.log.debug(f'{k}: {v}') for k, v in colvar.items()]


class tkhandler(logger.logging.Handler):
    def __init__(self, widget: tk.Text):
        logger.logging.Handler.__init__(self)
        self.widget = widget

    def emit(self, record: logger.logging.LogRecord):
        # Create list for temporary use
        tags = []

        # Get the current line in the widget (console)
        line = self.widget.index('end-1c').split('.')[0]

        # Iterate over every match defined by `tkpattern`
        for match in re.findall(tkpattern, record.message):
            # Match to the ascii escape sequence
            if color := re.match(tkmatch, match):
                col = color.group()  # color.group() gets the color code

                # Get the starting position of the first match
                start_pos = record.message.find(col)

                # string.find() will return -1 if no index was found.
                # If that happens, we skip the rest of this iteration.
                if start_pos == -1:
                    continue

                # Get the end position of our selection
                end_pos = start_pos - len(col) + len(match)

                # Remove ascii characters in this selection from the final message
                record.message = record.message[:start_pos] + record.message[start_pos + len(col):]

                # Append a tuple with the information for the tag to the list
                tags.append((col, f'{line}.{start_pos}', f'{line}.{end_pos}'))

        global scroll_pos
        old_pos = scroll_pos.lo

        self.widget.configure(state='normal')
        self.widget.insert(tk.END, record.message + '\n')

        limit = 500
        del_line = 0
        currline = int(self.widget.index('end-1c').split('.')[0])
        if int(currline > limit):
            del_line = currline - limit
            self.widget.delete(f'{del_line}.0', f'{del_line + 1}.0')

        self.widget.configure(state='disabled')

        line_count = currline - del_line
        scroll_line = old_pos * line_count
        if line_count - scroll_line <= 3:
            self.widget.see(tk.END)

        # # Append message (record) to the end of the widget
        # self.widget.insert(END, record.message + '\n')

        # # Set our cursor position in the widget to the end of the widget
        # self.widget.see(END)

        # Iterate over our `tags` list and add tags for the selections
        [self.widget.tag_add(x[0], x[1], x[2]) for x in tags if x[1] != x[2]]


class tkfilter(logger.logging.Filter):
    def filter(self, record: logger.logging.LogRecord):  # This is only because of how our logging is set up.
        if record.levelno >= 40:  # If error/critical
            record.message = trace.alert + record.message
        elif record.levelno >= 30:  # If warning
            record.message = trace.warn + record.message
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

        def scrollpos(y0, y1):
            global scroll_pos
            self.cscroll.set(y0, y1)
            scroll_pos = ScrollbarPosition(float(y0), float(y1))

        self.console.configure(yscrollcommand=scrollpos)
        # self.console.tag_configure('default', background='yellow')
        # self.console.tag_config()

        self.coords = Label(self.frame_left, text='XY: None, None', relief=RAISED)
        self.coords.grid(row=99, column=0, padx=5, pady=5)

        self.condex = Label(self.frame_left, text='XY: None, None', relief=RAISED)
        self.condex.grid(row=100, column=0, padx=5, pady=5)

        self.color_config()

        self.console.bind('<Motion>', self.position)

        tkhand = tkhandler(self.console)
        tkhand.addFilter(tkfilter())
        logger.log.addHandler(tkhand)

    def test(self):
        for x in self.console.tag_names(index=None):
            logger.log.debug(x)

    def random_color(self):
        k, v = random.choice(list(colvar.items()))
        logger.log.debug(k[0] + v)
        # # logger.log.debug(CURRENT)
        # t = self.console.index(CURRENT)
        # print(t)
        # self.console.tag_add(str(k), CURRENT, END)
        # if v: logger.log.debug(v)
        # pass

    def position(self, event):
        self.coords.config(text=f'XY: {event.x}, {event.y}')
        self.condex.config(text=f'{self.console.index(tk.INSERT)}')
        # Label(self.frame_left, text=f'XY: {event.x}, {event.y}', relief=RAISED).grid(row=99, column=0, padx=5, pady=5)

    def color_config(self):
        for k, v in colvar.items():
            if v:
                self.console.tag_configure(str(k[0]), foreground=str(v))
                self.console.tag_configure(str(k[1]), background=str(v))
            else:
                self.console.tag_configure(str(k), foreground='yellow')
        pass
        self.console.tag_configure('default', foreground='yellow')

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
        Button(self.toolbar, text="Random Color", command=self.random_color).grid(row=4, column=0, padx=5, pady=5, sticky=W + E + N + S)
        Button(self.toolbar, text="Test", command=self.test).grid(row=5, column=0, padx=5, pady=5, sticky=W + E + N + S)
        Button(self.toolbar, text="Spam Console", command=self.test2).grid(row=6, column=0, padx=5, pady=5, sticky='w' + 'e' + 'n' + 's')

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
            berry.start(ui=True)
        except Exception as exc:
            logger.log.exception(exc)


if __name__ == "__main__":
    stitches().run()
