from core import logger
import subprocess as sub
from tkinter import *
import tkinter as tk
from threading import Thread
import start as berry
import asyncio
import time
import sys
import os


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
    def filter(self, record):
        # Special cases for all of the different log levels after this
        # This is a huge mess and I hate everything about it
        record.time = f'{trace.reset}[{trace.time}{core.time.misc.Now.unix()}{trace.reset}]'
        record.end = f'{trace.reset}{trace.alert}'
        record.reset = f'{trace.reset}'

        record.thrcol = ''
        record.color = ''

        if record.levelno >= 40:  # If error/critical
            record.thrcol = trace.red.s
            record.color = trace.alert
        elif record.levelno >= 30:  # If warning
            record.thrcol = trace.red
            record.color = trace.warn
        elif record.levelno <= 10:
            record.thrcol = trace.cyan
        return True


class stitches():
    def __init__(self):
        self.app = Tk()
        self.frame_left = Frame(self.app, width=200, height=400, bg='#6f7676')
        self.frame_right = Frame(self.app, width=650, height=400, bg='#6f7676')
        self.toolbar = Frame(self.frame_left, width=180, height=185, bg='#6f7676')

        self.console = Text(self.frame_right, bg="black", fg="green")
        self.console.pack(side='left', padx=5, pady=5)
        # self.console.grid(row=0, column=0, padx=5, pady=5)

        self.cscroll = Scrollbar(self.frame_right, orient="vertical", command=self.console.yview)
        self.cscroll.pack(side="right", expand=True, fill="y")

        self.console.configure(yscrollcommand=self.cscroll.set)
        # self.console_scroll.configure(command=self.console.yview)
        # self.console['yscrollcommand'] = Scrollbar(self.app, command=self.console.yview).grid(row=0, column=1, sticky='nsew').set
        # scrollb.grid(row=0, column=1, sticky='nsew')
        # self.txt['yscrollcommand'] = scrollb.set
        # self.console = tk.scrolledtext.ScrolledText(self.frame_right, bg="black", fg="green")
        # tk.scrolledtext.ScrolledText()
        tkhand = tkhandler(self.console)  # .addFilter(tkfilter())
        logger.log.addHandler(tkhand)

    def run(self):
        self.app.title("Stitch")
        self.app.geometry('850x450')
        self.app.resizable(False, False)

        self.frame_left.grid(row=0, column=0, padx=10, pady=5)
        self.frame_right.grid(row=0, column=1, padx=10, pady=5)
        self.toolbar.grid(row=2, column=0, padx=5, pady=5)
        # self.frame_right.grid(row=0, column=1, padx=10, pady=5)
        # self.frame_right.pack(fill=BOTH, expand=YES)

        Label(self.frame_left, text="Stitch testing", relief=RAISED).grid(row=0, column=0, padx=5, pady=5)

        # self.console.grid(row=0, column=0, padx=5, pady=5)
        # self.console.pack(expand=True, fill='both')

        Label(self.toolbar, text="General", relief=RAISED, fg="white", bg="#1a1a1a",).grid(row=0, column=0, padx=5, pady=3, ipadx=40)

        # self.start_button = Button(self.toolbar, text="Start", command=lambda: Thread(target=self.start_program).start()).grid(row=1, column=0, padx=5, pady=5, sticky='w' + 'e' + 'n' + 's')
        # Button(self.toolbar, text="Start", command=self.start_program).grid(row=1, column=0, padx=5, pady=5, sticky='w' + 'e' + 'n' + 's')
        Button(self.toolbar, text="Test", command=self.test).grid(row=2, column=0, padx=5, pady=5, sticky='w' + 'e' + 'n' + 's')

        self.app.configure(bg='#212121')

        Thread(target=self.start_program, name='Stitch-UI', daemon=True).start()

        self.app.mainloop()

        return

    def test(self):
        logger.log.debug('testing frame widget thing')

    def start_program(self):
        try:
            berry.start()
        except Exception as exc:
            logger.log.exception(exc)


if __name__ == "__main__":
    stitches().run()
