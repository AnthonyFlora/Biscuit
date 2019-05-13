import tkinter as tk
import collections
from Display.BoxPlot import BoxPlot


def value_to_color(value):
    s = 255 - int(255 * value)
    r = s
    g = s
    b = s
    return '#%02x%02x%02x' % (r,g,b)


class GatewayModel():
    def __init__(self):
        self.gateway = ''
        self.essid = ''
        self.signal = ''

class Model():
    def __init__(self):
        self.gateways = collections.defaultdict(lambda: GatewayModel())

class Controller():
    def __init__(self, model):
        self.model = model


class SpeedTestFrame(tk.Frame):
    def __init__(self, parent, model):
        tk.Frame.__init__(self, parent)
        self.model = model
        self.pack()
        frame = tk.LabelFrame(text=' SpeedTest ')
        frame.pack(padx=10, pady=10)

        # self.gateway = collections.defaultdict(lambda: {})
        # tk.Label(frame, text='hello').grid(row=0, column=0)
        # tk.Label(frame, text='helloxxxxxx').grid(row=3, column=1)

        b = BoxPlot(frame, 1, 50)
        b.grid(row=0, column=2)
        [b.set_cell_color(0, c, value_to_color(c/b.num_cols)) for c in range(b.num_cols)]
        BoxPlot(frame, 1, 50).grid(row=1, column=2)
        BoxPlot(frame, 1, 50).grid(row=2, column=2)
        BoxPlot(frame, 1, 50).grid(row=3, column=2)

if __name__ == '__main__':
    print('hello')
    model = Model()

    controller = Controller(model)

    root = tk.Tk()
    a = SpeedTestFrame(root, model)
    a.pack()

    tk.mainloop()