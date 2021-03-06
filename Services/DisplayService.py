import Services.Service
import collections
import datetime
import time
import tkinter as tk
import threading
import Messages.GatewayBenchmarkRequest
import Messages.GatewayBenchmarkResults
import Messages.GatewayStatus
import Messages.GatewayStatusRequest
import Messages.ServiceStatus
import Messages.SystemUpdateRequest
import functools
import queue

# TODO display for last message, sent??
# TODO control to select specific APs

class DisplayService(Services.Service.Service):
    def __init__(self, gui):
        Services.Service.Service.__init__(self, 'DisplayService')
        self.gui = gui
        self.hosts = hosts
        self.gui.queue_callback(functools.partial(gui.set_callback_system_update_request, self.request_system_update))
        self.gui.queue_callback(functools.partial(gui.set_callback_request_benchmark, self.request_benchmark_status))
        self.setup_handler('/biscuit/Messages/GatewayStatus', self.on_receive_gateway_status)
        self.setup_handler('/biscuit/Messages/GatewayBenchmarkResults', self.on_receive_gateway_benchmark_results)
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
        if service == 'GatewayService' and status == 'OPERATIONAL':
            self.request_gateway_status(host)
            #self.request_benchmark_status(host)

    def on_receive_gateway_status(self, message):
        m = Messages.GatewayStatus.GatewayStatus()
        m.from_json(message)
        host = m.hostname
        address = m.access_point
        self.gui.queue_callback(functools.partial(gui.update_gateway_address, host, address))
        ping = m.survey_status[address].ping
        last_update = datetime.datetime.fromtimestamp(float(m.survey_status[address].last_update)).strftime('%Y-%m-%d %H:%M:%S')
        download = '%0.3f' % (float(m.survey_status[address].download) / (1024.0 * 1024.0))
        upload = '%0.3f' % (float(m.survey_status[address].upload) / (1024.0 * 1024.0))
        text = '%s : %s mb/s dn,  %s mb/s up, %s ms' % (last_update, download, upload, ping)
        self.gui.queue_callback(functools.partial(gui.update_benchmark_results, host, text))

    def on_receive_gateway_benchmark_results(self, message):
        m = Messages.GatewayBenchmarkResults.GatewayBenchmarkResults()
        m.from_json(message)
        host = m.hostname
        ping = m.ping
        last_update = datetime.datetime.fromtimestamp(float(m.last_update)).strftime('%Y-%m-%d %H:%M:%S')
        download = '%0.3f' % (float(m.download) / (1024.0 * 1024.0))
        upload = '%0.3f' % (float(m.upload) / (1024.0 * 1024.0))
        text = '%s : %s mb/s dn,  %s mb/s up, %s ms' % (last_update, download, upload, ping)
        self.gui.queue_callback(functools.partial(gui.update_benchmark_results, host, text))

    def request_system_update(self, host):
        m = Messages.SystemUpdateRequest.SystemUpdateRequest()
        m.hostname = host
        self.client.publish('/biscuit/Messages/SystemUpdateRequest', m.to_json(), qos=1)

    def request_gateway_status(self, host):
        m = Messages.GatewayStatusRequest.GatewayStatusRequest()
        m.hostname = host
        self.client.publish('/biscuit/Messages/GatewayStatusRequest', m.to_json(), qos=1)

    def request_benchmark_status(self, host, refresh=False):
        m = Messages.GatewayBenchmarkRequest.GatewayBenchmarkRequest()
        m.hostname = host
        m.refresh = refresh
        self.request_gateway_status(host)
        self.client.publish('/biscuit/Messages/GatewayBenchmarkRequest', m.to_json(), qos=1)



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
        self.labels = collections.defaultdict(lambda: tk.Label(self, text='UNKNOWN'))
        for irow in range(len(hosts)):
            host = hosts[irow]
            self.labels[host].grid(row=irow, column=0, sticky='news')

class ServiceUpdateFrame(tk.LabelFrame):
    def __init__(self, parent, hosts):
        tk.LabelFrame.__init__(self, parent, text=' Update ')
        self.buttons = collections.defaultdict(lambda: tk.Button(self, text='Update'))
        for irow in range(len(hosts)):
            host = hosts[irow]
            self.rowconfigure(irow, weight=1)
            self.buttons[host]['text'] = host
            self.buttons[host]['command'] = lambda host=host, parent=parent: parent.callback_system_update_request(host)
            self.buttons[host].grid(row=irow, column=0, sticky='news')

class BenchmarkUpdateFrame(tk.LabelFrame):
    def __init__(self, parent, hosts):
        tk.LabelFrame.__init__(self, parent, text=' Update ')
        self.buttons = collections.defaultdict(lambda: tk.Button(self, text='Update'))
        for irow in range(len(hosts)):
            host = hosts[irow]
            self.rowconfigure(irow, weight=1)
            self.buttons[host]['text'] = host
            self.buttons[host]['command'] = lambda host=host, parent=parent: parent.callback_request_benchmark(host, refresh=True)
            self.buttons[host].grid(row=irow, column=0, sticky='news')

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
                self.labels[host][service] = tk.Label(frame, text='UNKNOWN')
                self.labels[host][service].grid(row=irow, column=icol, sticky='news')

class GatewayAddressFrame(tk.LabelFrame):
    def __init__(self, parent, hosts):
        tk.LabelFrame.__init__(self, parent, text=' Address ')
        self.labels = collections.defaultdict(lambda: tk.Label(self, text='????'))
        for irow in range(len(hosts)):
            host = hosts[irow]
            self.labels[host].grid(row=irow, column=0, sticky='news')


class GatewayBenchmarkFrame(tk.LabelFrame):
    def __init__(self, parent, hosts):
        tk.LabelFrame.__init__(self, parent, text=' Benchmark ')
        self.labels = collections.defaultdict(lambda: tk.Label(self, text='????'))
        print(len(hosts))
        for irow in range(len(hosts)):
            host = hosts[irow]
            self.labels[host].grid(row=irow, column=0, stick='news')




class DisplayGUI(tk.Frame):
    def __init__(self, parent, hosts, services):
        tk.Frame.__init__(self, parent)
        self.winfo_toplevel().title("Biscuit - DisplayService")

        self.callback_system_update_request = None
        self.callback_request_benchmark = None

        HostNameFrame(self, hosts).grid(row=0, column=0, sticky='news')
        self.service_version_frame = ServiceVersionFrame(self, hosts)
        self.service_version_frame.grid(row=0, column=1, sticky='news')
        self.service_status_frame = ServiceStatusFrame(self, hosts, services)
        self.service_status_frame.grid(row=0, column=2, sticky='news', columnspan=5)
        self.service_update_frame = ServiceUpdateFrame(self, hosts)
        self.service_update_frame.grid(row=0, column=7, sticky='news')

        self.gateway_hostname_frame = HostNameFrame(self, hosts)
        self.gateway_hostname_frame.grid(row=1, column=0, sticky='news')
        self.gateway_address_frame = GatewayAddressFrame(self, hosts)
        self.gateway_address_frame.grid(row=1, column=1, sticky='news')
        self.gateway_benchmark_frame = GatewayBenchmarkFrame(self, hosts)
        self.gateway_benchmark_frame.grid(row=1, column=2, sticky='news', columnspan=5)
        self.benchmark_update_frame = BenchmarkUpdateFrame(self, hosts)
        self.benchmark_update_frame.grid(row=1, column=7, sticky='news')

        self.callbacks = queue.Queue()
        self.process_callbacks()

        self.pack(padx=5, pady=5)

    def set_callback_system_update_request(self, callback):
        self.callback_system_update_request = callback
        print('callback set system update')

    def set_callback_request_benchmark(self, callback):
        self.callback_request_benchmark = callback
        print('callback set request benchmark')

    def update_service_status(self, host, service, status):
        self.service_status_frame.labels[host][service]['text'] = status

    def update_service_version(self, host, version):
        self.service_version_frame.labels[host]['text'] = version

    def update_gateway_address(self, host, address):
        self.gateway_address_frame.labels[host]['text'] = address

    def update_benchmark_results(self, host, text):
        self.gateway_benchmark_frame.labels[host]['text'] = text

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
    hosts.append('gateway1')
    hosts.append('gateway2')
    hosts.append('gateway3')
    hosts.append('gateway4')

    services = []
    services.append('DefibrillatorService')
    services.append('WeatherService')
    services.append('DisplayService')
    services.append('GatewayService')
    services.append('HeartbeatService')

    services.append('SystemService')

    gui = DisplayGUI(tk.Tk(), hosts, services)
    threading.Thread(target=component_thread, args=(gui,)).start()
    tk.mainloop()

