import Services.Service
import collections
import datetime
import time
import tkinter as tk
from Config.Config import *
import threading
import Messages.ServiceStatus
import functools
import queue

class DisplayService(Services.Service.Service):
    def __init__(self, gui):
        Services.Service.Service.__init__(self, 'DisplayService')
        self.gui = gui
        self.setup_handler('/biscuit/Statuses/#', self.on_receive_service_status)

    def on_receive_service_status(self, message):
        m = Messages.ServiceStatus.ServiceStatus()
        m.from_json(message)
        host = m.hostname
        service = m.service
        status = m.status
        version = m.version
        self.gui.queue_callback(functools.partial(gui.update_service_status, host, service, status))
        self.gui.queue_callback(functools.partial(gui.update_service_version, host, version))


class HostNameFrame(tk.LabelFrame):
    def __init__(self, parent, hosts):
        tk.LabelFrame.__init__(self, parent, text=' Host ')
        self.labels = collections.defaultdict(lambda: tk.Label(self))
        for irow in range(len(hosts)):
            host = hosts[irow]
            self.labels[host] = tk.Label(self, text=host)
            self.labels[host].grid(row=irow, column=0)

class ServiceVersionFrame(tk.LabelFrame):
    def __init__(self, parent, hosts):
        tk.LabelFrame.__init__(self, parent, text=' Version ')
        self.labels = collections.defaultdict(lambda: tk.Label(self))
        for irow in range(len(hosts)):
            host = hosts[irow]
            self.labels[host] = tk.Label(self, text='????')
            self.labels[host].grid(row=irow, column=0)


class ServiceStatusFrame(tk.Frame):
    def __init__(self, parent, hosts, services):
        tk.Frame.__init__(self, parent)
        self.labels = collections.defaultdict(lambda: collections.defaultdict(lambda: tk.Label(self)))
        for icol in range(len(services)):
            service = services[icol]
            frame = tk.LabelFrame(self, text=' ' + service + ' ')
            frame.grid(row=0, column=icol)
            for irow in range(len(hosts)):
                host = hosts[irow]
                self.labels[host][service] = tk.Label(frame, text='OFFLINE')
                self.labels[host][service].grid(row=irow, column=icol)


class GatewayEssidFrame(tk.LabelFrame):
    def __init__(self, parent, hosts):
        tk.LabelFrame.__init__(self, parent, text=' ESSID ')
        self.labels = collections.defaultdict(lambda: tk.Label(self))
        for irow in range(len(hosts)):
            host = hosts[irow]
            self.labels[host] = tk.Label(self, text='????')
            self.labels[host].grid(row=irow, column=0)


class DisplayGUI(tk.Frame):
    def __init__(self, parent, hosts, services):
        tk.Frame.__init__(self, parent)

        HostNameFrame(self, hosts).grid(row=0, column=0)
        self.service_version_frame = ServiceVersionFrame(self, hosts)
        self.service_version_frame.grid(row=0, column=1)
        self.service_status_frame = ServiceStatusFrame(self, hosts, services)
        self.service_status_frame.grid(row=0, column=2)

        HostNameFrame(self, hosts).grid(row=1, column=0)
        self.gateway_essid_frame = GatewayEssidFrame(self, hosts)
        self.gateway_essid_frame.grid(row=1, column=1)
        self.callbacks = queue.Queue()
        self.process_callbacks()

        self.pack(padx=5, pady=5)

    def update_service_status(self, host, service, status):
        self.service_status_frame.labels[host][service]['text'] = status

    def update_service_version(self, host, version):
        self.service_version_frame.labels[host]['text'] = version

    def queue_callback(self, callback):
        self.callbacks.put(callback)

    def process_callbacks(self):
        while not self.callbacks.empty():
            callback = self.callbacks.get()
            callback()
        self.after(10, self.process_callbacks)


def component_thread(gui):
    while True: # TODO dont restart if GUI closed
        try:
            DisplayService(gui).run()
        except:
            None
        print(str(datetime.datetime.now()), 'Restarting DisplayService..')
        time.sleep(10.0)


if __name__== '__main__':

    hosts = []
    hosts.append('hyperion')
    hosts.append('gateway')

    services = []
    services.append('DefibrillatorService')
    services.append('DisplayService')
    services.append('GatewayService')
    services.append('HeartbeatService')
    services.append('SystemService')

    gui = DisplayGUI(tk.Tk(), hosts, services)
    threading.Thread(target=component_thread, args=(gui,)).start()
    tk.mainloop()

