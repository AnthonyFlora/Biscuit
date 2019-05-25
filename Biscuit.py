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


class GatewayStatusFrame(tk.Label):
    def __init__(self, parent, model):
        tk.Label.__init__(self, parent)
        self.model = model
        self.name_frame = tk.LabelFrame(self, text=' Gateway ')
        self.name_frame.grid(row=0, column=0)
        self.labels = collections.defaultdict(lambda: tk.Label(self, text='???'))
        self.labels['0'].grid(row=0, column=0)
        self.labels['1'].grid(row=1, column=0)
        self.labels['2'].grid(row=2, column=0)
        self.labels['3'].grid(row=3, column=0)


class GatewayControlFrame(tk.LabelFrame):
    def __init__(self, parent, model):
        tk.LabelFrame.__init__(self, parent, text=' Control ')
        self.model = model

        b = BoxPlot(self, 1, 50)
        b.grid(row=0, column=2)
        [b.set_cell_color(0, c, value_to_color(c/b.num_cols)) for c in range(b.num_cols)]
        BoxPlot(self, 1, 50).grid(row=1, column=2)
        BoxPlot(self, 1, 50).grid(row=2, column=2)
        BoxPlot(self, 1, 50).grid(row=3, column=2)


if __name__ == '__main__':
    print('hello')
    model = Model()
    model.gateways['hyperion']
    model.gateways['gateway']

    controller = Controller(model)

    root = tk.Tk()
    GatewayStatusFrame(root, model).grid(row=0, column=0, padx=5, pady=5)
    GatewayControlFrame(root, model).grid(row=0, column=1, padx=5, pady=5)

    tk.mainloop()