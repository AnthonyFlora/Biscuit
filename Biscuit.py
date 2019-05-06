import tkinter as tk
import threading
import time
from Config.Config import *


class Biscuit(tk.Frame):
    def __init__(self, parent=None, data=0.5):
        tk.Frame.__init__(self, parent, background=GUI_BACKGROUND)
        self.canvas = tk.Canvas(self, highlightbackground=GUI_BACKGROUND)
        self.canvas.bind('<Configure>', self.on_resize)
        self.canvas.grid(sticky='news')
        self.canvas.pack(fill='both', expand=1)
        self.progress_made = self.canvas.create_rectangle(0, 0, 1, 1, fill=GUI_PROGRESS_BAR_PROGRESS_MADE)
        self.progress_left = self.canvas.create_rectangle(0, 0, 1, 1, fill=GUI_PROGRESS_BAR_PROGRESS_LEFT)
        self.data = data
        self.data_stale = True
        self.pack(fill='both', expand=1)

if __name__ == '__main__':
    root = tk.Tk()
    plot = Biscuit(root)
    tk.mainloop()