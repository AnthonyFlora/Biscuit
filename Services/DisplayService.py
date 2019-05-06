import Services.Service
import collections
from Common import Observable
import datetime
import time
import tkinter as tk
from Config.Config import *
import threading

class DisplayService(Services.Service.Service):
    def __init__(self, model):
        Services.Service.Service.__init__(self, 'DisplayService')
        self.model = model
        self.model.data['moo'].update('555')

class DisplayModel():
    def __init__(self):
        self.data = collections.defaultdict(lambda: Observable.Observable())
        self.data['moo'].update('init')

class DisplayGUI(tk.Frame):
    def __init__(self, parent, model):
        tk.Frame.__init__(self, parent, background=GUI_BACKGROUND)
        self.label = tk.Label(self, text='hiii')
        self.label.pack()
        self.pack()
        self.model = model
        self.model.data['moo'].observe(self.update)

    def update(self, text):
        self.label['text'] = text

def component_thread(model):
    while True:
        try:
            component = DisplayService(model)
            component.run()
        except:
            None
        print(str(datetime.datetime.now()), 'Restarting DisplayService..')
        time.sleep(10.0)

if __name__ == '__main__':
    model = DisplayModel()
    gui = DisplayGUI(tk.Tk(), model)
    threading.Thread(target=component_thread, args=(model,)).start()
    tk.mainloop()

