import tkinter as tk

class BoxPlot(tk.Frame):
    def __init__(self, parent=None, num_rows=10, num_cols=10):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, background='white')
        self.canvas.bind('<Configure>', self.on_resize)
        self.canvas.grid(sticky='news')
        self.canvas.pack(fill='both', expand=1)
        self.boxes = [[self.canvas.create_rectangle(0, 0, 1, 1) for c in range(num_cols)] for r in range(num_rows)]
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.is_stale_size = False
        self.pack(fill='both', expand=1)

    def on_resize(self, event):
        self.is_stale_size = True
        self.replot()

    def set_data_cell(self, row, col, color):
        self.canvas.itemconfig(self.boxes[row][col], fill=color)
        self.after_idle(self.replot)

    def set_data_col(self, col, color):
        [self.canvas.itemconfig(self.boxes[row][col], fill=color) for row in range(self.num_rows)]

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

if __name__ == '__main__':
    print('hello')
    root = tk.Tk()
    plot = BoxPlot(root)
    plot.set_data_cell(3, 5, 'red')
    tk.mainloop()