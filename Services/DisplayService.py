import Services.Service
import collections
from Common import Observable
import datetime
import time
import tkinter as tk
from Config.Config import *
import threading
import Messages.ServiceStatus

class DisplayService(Services.Service.Service):
    def __init__(self, model):
        Services.Service.Service.__init__(self, 'DisplayService')
        self.model = model
        self.setup_handler('/biscuit/Statuses/#', self.on_receive_service_status)

    def on_receive_service_status(self, message):
        m = Messages.ServiceStatus.ServiceStatus()
        m.from_json(message)
        self.model.state['service_statuses'].data[m.hostname + ':' + m.service] = m
        self.model.state['service_statuses'].notify()
        print(m.model.state['service_statuses'])

class DisplayModel():
    def __init__(self):
        self.state = collections.defaultdict(lambda: Observable.Observable())
        self.state['service_statuses'].update(collections.defaultdict(lambda: ''))

class DisplayGUI(tk.Frame):
    def __init__(self, parent, model):
        tk.Frame.__init__(self, parent, background=GUI_BACKGROUND)
        self.label = tk.Label(self, text='hiii')
        self.label.pack()
        self.pack()
        self.model = model
        self.model.state['service_statuses'].observe(self.update_service_status)

    def update_service_status(self, text):
        self.label['text'] = text
        for k,v in self.model.state['service_statuses'].data.items():
            print(v.hostname + ' : ' + v.service  + ' --> ' + v.status + ' @ ' + v.version)


def component_thread(model):
    while True:
        try:
            DisplayService(model).run()
        except:
            None
        print(str(datetime.datetime.now()), 'Restarting DisplayService..')
        time.sleep(10.0)


if __name__ == '__main__':
    model = DisplayModel()
    gui = DisplayGUI(tk.Tk(), model)
    threading.Thread(target=component_thread, args=(model,)).start()
    tk.mainloop()

