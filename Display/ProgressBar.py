import tkinter as tk
from Config.Config import *


class ProgressBar(tk.Frame):
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

    def update(self, data):
        self.data = data
        self.data_stale = True

    def on_resize(self, event):
        self.replot()

    def replot(self):
        if self.data_stale:
            w = self.winfo_width()
            h = self.winfo_height()
            self.canvas.coords(self.progress_made, 0, 0, w * self.data, h)
            self.canvas.coords(self.progress_left, w * self.data, 0, w, h)
            self.data_stale = False
        self.after(GUI_REFRESH_RATE_MS, self.replot)


if __name__ == '__main__':
    root = tk.Tk()
    plot = ProgressBar(root)
    tk.mainloop()