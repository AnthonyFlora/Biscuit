import tkinter as tk

class BoxPlot(tk.Frame):
    def __init__(self, parent=None, num_rows=10, num_cols=10, grid_row=0, grid_col=0):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width=600, height=25, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.bind('<Configure>', self.on_resize)
        self.canvas.grid(sticky='news')
        self.canvas.pack(fill='both', expand=1)
        self.boxes = [[self.canvas.create_rectangle(0, 0, 1, 1) for c in range(num_cols)] for r in range(num_rows)]
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.is_stale_size = False
        #self.pack(fill='both', expand=1)

    def on_resize(self, event):
        self.is_stale_size = True
        self.replot()

    def set_cell_color(self, row, col, color):
        self.canvas.itemconfig(self.boxes[row][col], fill=color)
        self.after_idle(self.replot)

    def set_row_color(self, row, color):
        [self.canvas.itemconfig(self.boxes[row][col], fill=color) for col in range(self.num_cols)]

    def set_col_color(self, col, color):
        [self.canvas.itemconfig(self.boxes[row][col], fill=color) for row in range(self.num_rows)]

    def set_all_color(self, color):
        [self.set_data_col(col, color) for col in range(self.num_cols)]

    def replot(self):
        if self.is_stale_size:
            self.update_size()
            self.is_stale_size = False

    def update_size(self):
        border_offset = 6
        w = (self.winfo_width() - border_offset) / self.num_cols
        h = (self.winfo_height() - border_offset ) / self.num_rows
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.canvas.coords(self.boxes[row][col], w*col+border_offset/2, h*row+border_offset/2, w*col+w, h*row+h)


def value_to_color(value):
    s = 255 - int(255 * value)
    r = s
    g = s
    b = s
    return '#%02x%02x%02x' % (r,g,b)

if __name__ == '__main__':
    print('hello')
    root = tk.Tk()
    frame = tk.LabelFrame(text=' Speedtest ')
    frame.pack(padx=10, pady=10)

    tk.Label(frame, text='hello').grid(row=0, column=0)
    tk.Label(frame, text='helloxx').grid(row=1, column=0)
    tk.Label(frame, text='helloxxxx').grid(row=2, column=0)
    tk.Label(frame, text='helloxxxxxx').grid(row=3, column=0)

    tk.Label(frame, text='hello').grid(row=0, column=1)
    tk.Label(frame, text='helloxx').grid(row=1, column=1)
    tk.Label(frame, text='helloxxxx').grid(row=2, column=1)
    tk.Label(frame, text='helloxxxxxx').grid(row=3, column=1)

    b = BoxPlot(frame, 1, 25)
    b.grid(row=0, column=2)
    BoxPlot(frame, 1, 25).grid(row=1, column=2)
    BoxPlot(frame, 1, 25).grid(row=2, column=2)
    BoxPlot(frame, 1, 25).grid(row=3, column=2)

    [b.set_cell_color(0, c, value_to_color(c/b.num_cols)) for c in range(b.num_cols)]
    tk.mainloop()