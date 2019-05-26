import Services.Service
import collections
import datetime
import time
import tkinter as tk
import threading
import Display.BoxPlot
import Messages.GatewayStatus
import Messages.GatewayStatusRequest
import Messages.ServiceStatus
import functools
import queue

class DisplayService(Services.Service.Service):
    def __init__(self, gui):
        Services.Service.Service.__init__(self, 'DisplayService')
        self.gui = gui
        self.hosts = hosts
        self.setup_handler('/biscuit/Statuses/#', self.on_receive_service_status)
        self.setup_handler('/biscuit/Messages/GatewayStatus', self.on_receive_gateway_status)

    def on_receive_service_status(self, message):
        m = Messages.ServiceStatus.ServiceStatus()
        m.from_json(message)
        host = m.hostname
        service = m.service
        status = m.status
        version = m.version
        self.gui.queue_callback(functools.partial(gui.update_service_status, host, service, status))
        self.gui.queue_callback(functools.partial(gui.update_service_version, host, version))
        if service == 'GatewayService':
            self.request_gateway_status(host)

    def on_receive_gateway_status(self, message):
        m = Messages.GatewayStatus.GatewayStatus()
        m.from_json(message)
        host = m.hostname
        address = m.access_point_address
        self.gui.queue_callback(functools.partial(gui.update_gateway_address, host, address))

    def request_gateway_status(self, host):
        m = Messages.GatewayStatusRequest.GatewayStatusRequest()
        m.hostname = host
        self.client.publish('/biscuit/Messages/GatewayStatusRequest', m.to_json(), qos=1)


class HostNameFrame(tk.LabelFrame):
    def __init__(self, parent, hosts):
        tk.LabelFrame.__init__(self, parent, text=' Host ')
        self.labels = collections.defaultdict(lambda: tk.Label(self, text='????'))
        for irow in range(len(hosts)):
            host = hosts[irow]
            self.labels[host]['text'] = host
            self.labels[host].grid(row=irow, column=0, sticky='news')

class ServiceVersionFrame(tk.LabelFrame):
    def __init__(self, parent, hosts):
        tk.LabelFrame.__init__(self, parent, text=' Version ')
        self.labels = collections.defaultdict(lambda: tk.Label(self, text='????'))
        for irow in range(len(hosts)):
            host = hosts[irow]
            self.labels[host].grid(row=irow, column=0, sticky='news')


class ServiceStatusFrame(tk.Frame):
    def __init__(self, parent, hosts, services):
        tk.Frame.__init__(self, parent)
        self.labels = collections.defaultdict(lambda: collections.defaultdict(lambda: tk.Label(self, text='????')))
        for icol in range(len(services)):
            service = services[icol]
            frame = tk.LabelFrame(self, text=' ' + service + ' ')
            frame.grid(row=0, column=icol, sticky='news')
            for irow in range(len(hosts)):
                host = hosts[irow]
                self.labels[host][service] = tk.Label(frame, text='OFFLINE')
                self.labels[host][service].grid(row=irow, column=icol, sticky='news')


class GatewayAddressFrame(tk.LabelFrame):
    def __init__(self, parent, hosts):
        tk.LabelFrame.__init__(self, parent, text=' Address ')
        self.labels = collections.defaultdict(lambda: tk.Label(self, text='????'))
        for irow in range(len(hosts)):
            host = hosts[irow]
            self.labels[host].grid(row=irow, column=0, sticky='news')


class GatewaySpeedtestFrame(tk.LabelFrame):
    def __init__(self, parent, hosts):
        tk.LabelFrame.__init__(self, parent, text=' Speedtest ')
        self.plot = collections.defaultdict(lambda: Display.BoxPlot.BoxPlot(self, 1, 50))
        for irow in range(len(hosts)):
            host = hosts[irow]
            self.plot[host].grid(row=irow, column=0, stick='news')


class DisplayGUI(tk.Frame):
    def __init__(self, parent, hosts, services):
        tk.Frame.__init__(self, parent)

        HostNameFrame(self, hosts).grid(row=0, column=0, sticky='news')
        self.service_version_frame = ServiceVersionFrame(self, hosts)
        self.service_version_frame.grid(row=0, column=1, sticky='news')
        self.service_status_frame = ServiceStatusFrame(self, hosts, services)
        self.service_status_frame.grid(row=0, column=2, sticky='news')

        HostNameFrame(self, hosts).grid(row=1, column=0, sticky='news')
        self.gateway_address_frame = GatewayAddressFrame(self, hosts)
        self.gateway_address_frame.grid(row=1, column=1, sticky='news')
        self.gateway_speedtest_frame = GatewaySpeedtestFrame(self, hosts)
        self.gateway_speedtest_frame.grid(row=1, column=2, sticky='news')
        self.gateway_speedtest_frame.columnconfigure(0, weight=1)
        self.gateway_speedtest_frame.rowconfigure(0, weight=1)

        self.callbacks = queue.Queue()
        self.process_callbacks()

        self.pack(padx=5, pady=5)

    def update_service_status(self, host, service, status):
        self.service_status_frame.labels[host][service]['text'] = status

    def update_service_version(self, host, version):
        self.service_version_frame.labels[host]['text'] = version

    def update_gateway_address(self, host, address):
        self.gateway_address_frame.labels[host]['text'] = address

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

