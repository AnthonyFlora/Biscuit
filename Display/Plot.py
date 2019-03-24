import tkinter as tk

class Plot(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, background='white')
        self.canvas.bind('<Configure>', self.on_resize)
        self.canvas.grid(sticky='news')
        self.canvas.pack(fill='both', expand=1)
        self.data = {}
        self.ylim_min = None
        self.ylim_max = None
        self.xlim_min = None
        self.xlim_max = None
        self.is_stale = False

    def on_resize(self, event):
        self.is_stale = True
        self.replot()

    def set_ylim(self, ylim_min, ylim_max):
        self.ylim_min = ylim_min
        self.ylim_max = ylim_max
        self.replot()

    def set_xlim(self, xlim_min, xlim_max):
        self.xlim_min = xlim_min
        self.xlim_max = xlim_max
        self.replot()

    def set_color(self, tag, color):
        if tag in self.data:
            self.canvas.itemconfigure(tag, fill=color)

    def set_data(self, tag, data):
        if tag in self.data and data is None:
            self.data.pop(tag)
            self.canvas.delete(tag)
        if tag in self.data and data is not None:
            self.data[tag] = data
        if tag not in self.data and data is not None:
            self.data[tag] = data
            self.canvas.create_line((0, 0, 0, 0), tag=tag, fill='black', width=1)
        self.is_stale = True
        self.after_idle(self.replot)

    def get_xy_limits(self):
        mx_min = self.xlim_min
        if mx_min is None:
            mx_min = 0
            for k, v in self.data.items():
                mx_min = min(mx_min, len(v))
        mx_max = self.xlim_max
        if mx_max is None:
            mx_max = 0
            for k, v in self.data.items():
                mx_max = max(mx_max, len(v))
        my_min = self.ylim_min
        if my_min is None:
            my_min = 0
            for k, v in self.data.items():
                my_min = min(my_min, min(v))
        my_max = self.ylim_max
        if my_max is None:
            my_max = 0
            for k, v in self.data.items():
                my_max = max(my_max, max(v))
        return mx_min, mx_max, my_min, my_max

    def replot(self):
        if not self.is_stale:
            return
        self.is_stale = False
        w = self.winfo_width()
        h = self.winfo_height()
        mx_min, mx_max, my_min, my_max = self.get_xy_limits()
        mx = mx_max - mx_min
        my = my_max - my_min
        print('[%d %d] [%d %d]' % (mx_min, mx_max, my_min, my_max))
        for k,v in self.data.items():
            coords = []
            for n in range(0, len(v)):
                x = (w * n) / (mx - 1)
                coords.append(x)
                coords.append(h - ((h / my) * v[n] - my_min))
            self.canvas.coords(k, *coords)
