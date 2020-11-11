from core.logger import log, json
from tkinter import *
import tkinter as tk
import time
import sys
import os


class stitches():
    def __init__(self):
        self.app = Tk()
        self.frame_right = Frame(self.app, width=650, height=400, bg='#6f7676')
        self.console = Text(self.frame_right, bg="black", fg="green")

    def run(self):
        self.app.title("Stitch")
        self.app.geometry('850x450')
        self.app.resizable(False, False)

        self.frame_right.grid(row=0, column=1, padx=10, pady=5)
        self.frame_right.pack(fill=BOTH, expand=YES)

        self.console.grid(row=0, column=0, padx=5, pady=5)
        self.console.insert(END, f"Test1\n")
        self.console.insert(END, f"Test2\n")

        self.app.configure(bg='#212121')

        self.app.mainloop()
        return


if __name__ == "__main__":
    stitches().run()
