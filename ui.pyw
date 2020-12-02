from core.color import trace
from core import logger
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


""" Convert colorama colors to tkinter colors """
colvar = {

}


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
                color = color.group()
                print(color)
                # self.widget.tag_add('default', '5.0')
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

        tkhand = tkhandler(self.console)
        tkhand.addFilter(tkfilter(self.console))
        logger.log.addHandler(tkhand)

    def color_config(self):
        foregrounds = {

        }
        backgrounds = {

        }
        # self.console.tag_configure('default', )

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

        self.app.configure(bg='#212121')

        threading.Thread(target=self.start_program, name=f'{name}-UI', daemon=True).start()

        self.app.mainloop()

        return

    def test(self):
        logger.log.debug('testing frame widget thing')
        Button(self.toolbar, text="Test2", command=self.test2).grid(row=3, column=0, padx=5, pady=5, sticky='w' + 'e' + 'n' + 's')

    def test2(self):
        logger.log.debug('Will this run?')

    def start_program(self):
        try:
            berry.start()
        except Exception as exc:
            logger.log.exception(exc)


if __name__ == "__main__":
    stitches().run()
