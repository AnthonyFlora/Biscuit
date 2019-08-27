#! python

import Config.Config
import collections
import threading
import tkinter as tk
import paho.mqtt.client as mqtt
from tkinter import ttk
import Messages.ServiceStatus
import Messages.WeatherReport
import Messages.GatewayStatus
import Messages.GatewayStatusRequest
import datetime
import time
import collections


DEFAULT_COLOR_BACKGROUND = '#3c3f41'
DEFAULT_COLOR_STATUS_BACKGROUND = '#24568b'
DEFAULT_COLOR_CONTENT_BACKGROUND = '#f2f2f2'
DEFAULT_COLOR_NAVIGATION_BACKGROUND = '#18395b'


class Controller(threading.Thread):
    def __init__(self, display):
        threading.Thread.__init__(self)
        self.daemon = True
        self.display = display
        self.status_frame = display.status_frame

    def run(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_receive
        self.client.on_disconnect = self.on_disconnect
        while True:
            try:
              self.client.connect(Config.Config.DEFAULT_BROKER, 1883, keepalive=5)
              self.client.loop_forever()
            except Exception as e:
              print(str(e))
            time.sleep(1)

    def on_connect(self, client, userdata, flags, rc):
        self.status_frame.set_connection_status('Connected')
        self.client.subscribe('/biscuit/Statuses/#', qos=1)
        self.client.subscribe('/biscuit/Messages/#', qos=1)

    def on_disconnect(self, client, userdata, rc):
        self.status_frame.set_connection_status('Disconnected')
        print('Disconnected')

    def on_receive(self, client, userdata, message):
        try:
            print('Received %s' % message.topic)
            if '/Statuses/' in message.topic:
                m = Messages.ServiceStatus.ServiceStatus()
                m.from_json(message.payload.decode('utf-8'))
                self.display.summary_frame.service_status_view.update(m.hostname, m.version, m.service, m.status)
                if m.service == 'GatewayService':
                    if m.status == 'OPERATIONAL':
                        gateway_status_request = Messages.GatewayStatusRequest.GatewayStatusRequest()
                        gateway_status_request.hostname = m.hostname
                        self.client.publish('/biscuit/Messages/GatewayStatusRequest', gateway_status_request.to_json(), qos=1)
                    else:
                        print('got non-op gateway status')
                        self.display.gateway_frame.site_survey_view.clear(m.hostname)
            elif '/Messages/' in message.topic:
                if 'WeatherReport' in message.topic:
                    m = Messages.WeatherReport.WeatherReport()
                    m.from_json(message.payload.decode('utf-8'))
                    for sensor, weather in m.weather_updates.items():
                        self.display.summary_frame.weather_report_view.update(sensor, weather.temperature, weather.humidity, m.last_update)
                elif 'GatewayStatusRequest' in message.topic:
                    print(message.payload)
                elif 'GatewayStatus' in message.topic:
                    print(message.payload)
                    m = Messages.GatewayStatus.GatewayStatus()
                    m.from_json(message.payload.decode('utf-8'))
                    for access_point, survey in m.survey_status.items():
                        self.display.gateway_frame.site_survey_view.update(access_point, m.hostname, survey.download)
        except Exception as e:
            print(str(e))

class FixedSizeLabel(tk.Frame):
    def __init__(self, parent, width, height, *args, **kwargs):
        tk.Frame.__init__(self, parent, width=width, height=height)
        self.pack_propagate(False)
        self.label = tk.Label(self, *args, **kwargs)
        self.label.pack(fill=tk.BOTH, expand=1)


class WeatherReportTreeView(tk.ttk.Treeview):
    def __init__(self, parent):
        tk.ttk.Treeview.__init__(self, parent, height=5)
        self['columns'] =  ('temperature', 'humidity', 'last_update')
        self.heading("#0", text='sensor', anchor='w')
        self.column("#0", anchor="w")
        self.heading('temperature', text='temperature')
        self.column('temperature', anchor='center', width=100)
        self.heading('humidity', text='humidity')
        self.column('humidity', anchor='center', width=100)
        self.heading('last_update', text='last_update')
        self.column('last_update', anchor='center', width=200)

    def update(self, sensor, temperature, humidity, last_update):
        children = self.get_children('')
        last_update = datetime.datetime.fromtimestamp(last_update).strftime('%Y-%m-%d %H:%M:%S')
        for child in children:
            if sensor == self.item(child, 'text'):
                self.item(child, values=(temperature, humidity, last_update))
                return
        self.insert('', 0, text=sensor, values=(temperature, humidity, last_update))


class ServiceStatusView(tk.ttk.Treeview):
    def __init__(self, parent):
        tk.ttk.Treeview.__init__(self, parent, height=26)
        self['columns'] =  ('version', 'status')
        self.heading("#0", text='service', anchor='w')
        self.column("#0", anchor="w")
        self.heading('version', text='version')
        self.column('version', anchor='center', width=100)
        self.heading('status', text='status')
        self.column('status', anchor='center', width=200)

    def update(self, hostname, version, service, status):
        children = self.get_children('')
        host_branch = None
        for child in children:
            if hostname == self.item(child, 'text'):
                host_branch = child
                break
        if not host_branch:
            host_branch = self.insert('', 'end', text=hostname, open=True)
        for host_child in self.get_children(host_branch):
            if service == self.item(host_child, 'text'):
                self.item(host_child, values=(version, status))
                return
        self.insert(host_branch, 'end', text=service, values=(version, status))


class SiteSurveyView(tk.ttk.Treeview):
    def __init__(self, parent):
        tk.ttk.Treeview.__init__(self, parent, height=32)
        self['columns'] =  ('gateway1', 'gateway2', 'gateway3', 'gateway4')
        self.heading("#0", text='access_point', anchor='w')
        self.column("#0", anchor="w")
        self.heading('gateway1', text='gateway1')
        self.column('gateway1', anchor='center', width=100)
        self.heading('gateway2', text='gateway2')
        self.column('gateway2', anchor='center', width=100)
        self.heading('gateway3', text='gateway3')
        self.column('gateway3', anchor='center', width=100)
        self.heading('gateway4', text='gateway4')
        self.column('gateway4', anchor='center', width=100)

    def clear(self, gateway):
        print('clearing', gateway)
        signals = collections.defaultdict(lambda: '')
        children = self.get_children('')
        for child in children:
            signals['gateway1'] = self.item(child)['values'][0]
            signals['gateway2'] = self.item(child)['values'][1]
            signals['gateway3'] = self.item(child)['values'][2]
            signals['gateway4'] = self.item(child)['values'][3]
            signals[gateway] = ''
            self.item(child, text=self.item(child, 'text'), values=(signals['gateway1'], signals['gateway2'], signals['gateway3'], signals['gateway4']))

        print('cleared')

    def update(self, access_point, gateway, signal):
        print('updating', gateway, access_point)
        signals = collections.defaultdict(lambda: '')
        children = self.get_children('')
        for child in children:
            if access_point == self.item(child, 'text'):
                signals['gateway1'] = self.item(child)['values'][0]
                signals['gateway2'] = self.item(child)['values'][1]
                signals['gateway3'] = self.item(child)['values'][2]
                signals['gateway4'] = self.item(child)['values'][3]
                signals[gateway] = signal
                self.item(child, values=(signals['gateway1'], signals['gateway2'], signals['gateway3'], signals['gateway4']))
                return
        signals[gateway] = signal
        self.insert('', 0, text=access_point, values=(signals['gateway1'], signals['gateway2'], signals['gateway3'], signals['gateway4']))


class DisplayFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background='#3c3f41', height=200, width=200)
        self.winfo_toplevel().title('Biscuit')
        self.navigation_frame = NavigationFrame(self)
        self.content_frame = ContentFrame(self)
        self.status_frame = StatusFrame(self)
        self.navigation_frame.grid(row=1, column=0, rowspan=1, columnspan=1, sticky='news')
        self.content_frame.grid(row=1, column=1, rowspan=1, columnspan=1, sticky='news')
        self.status_frame.grid(row=2, column=0, rowspan=1, columnspan=2, sticky='news')
        self.summary_frame = SummaryFrame(self)
        self.add_content('Summary', self.summary_frame)
        self.gateway_frame = GatewayFrame(self)
        self.add_content('Gateway', self.gateway_frame)
        self.weather_frame = WeatherFrame(self)
        self.add_content('Weather', self.weather_frame)
        self.security_frame = SecurityFrame(self)
        self.add_content('Security', self.security_frame)
        self.settings_frame = SettingsFrame(self)
        self.add_content('Settings', self.settings_frame)
        self.pack()
        self.navigation_frame.show_content('Summary')

    def add_content(self, title, frame):
        self.navigation_frame.add_content(title, frame)
        frame.grid(row=1, column=1, rowspan=1, columnspan=1, sticky='news')

class NavigationFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background=DEFAULT_COLOR_NAVIGATION_BACKGROUND, height=600, width=50)
        self.content_label_frame = collections.defaultdict(lambda: None)
        self.next_row = 0

    def add_content(self, title, frame):
        label = FixedSizeLabel(self, 100, 50, bg=DEFAULT_COLOR_NAVIGATION_BACKGROUND, fg='white', text=title, borderwidth=2)
        label.grid(row=self.next_row, column=0)
        label.label.bind("<Button-1>", lambda click_info: self.show_content(title))
        self.content_label_frame[title] = (label, frame)
        self.next_row = self.next_row + 1

    def show_content(self, title):
        for k, v in self.content_label_frame.items():
            v[0].label['text'] = k
        self.content_label_frame[title][0].label['text'] = '> ' + title
        self.content_label_frame[title][1].tkraise()
        print(title)


class ContentFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=DEFAULT_COLOR_CONTENT_BACKGROUND, height=600, width=900)


class SummaryFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=DEFAULT_COLOR_CONTENT_BACKGROUND, height=600, width=900)
        self.weather_report_view = WeatherReportTreeView(self)
        self.weather_report_view.pack(fill='x')
        self.service_status_view = ServiceStatusView(self)
        self.service_status_view.pack(fill='x')


class GatewayFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=DEFAULT_COLOR_CONTENT_BACKGROUND, height=600, width=900)
        self.site_survey_view = SiteSurveyView(self)
        self.site_survey_view.pack(fill='x')

class WeatherFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=DEFAULT_COLOR_CONTENT_BACKGROUND, height=600, width=900)


class SecurityFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=DEFAULT_COLOR_CONTENT_BACKGROUND, height=600, width=900)

class SettingsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=DEFAULT_COLOR_CONTENT_BACKGROUND, height=600, width=900)


class StatusFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background=DEFAULT_COLOR_STATUS_BACKGROUND, height=20, width=1000)
        self.status_label = tk.Label(self, text='Disconnected', fg='white', bg=DEFAULT_COLOR_STATUS_BACKGROUND)
        self.status_label.pack()

    def set_connection_status(self, connection_status):
        self.status_label['text'] = connection_status

if __name__ == '__main__':
    d = DisplayFrame(tk.Tk())
    c = Controller(d)
    c.start()

    tk.mainloop()
