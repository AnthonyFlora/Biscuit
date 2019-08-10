#! python

import Config.Config
import collections
import threading
import tkinter as tk
import paho.mqtt.client as mqtt

DEFAULT_COLOR_BACKGROUND = '#3c3f41'
DEFAULT_COLOR_STATUS_BACKGROUND = '#24568b'
DEFAULT_COLOR_CONTENT_BACKGROUND = '#f2f2f2'
DEFAULT_COLOR_NAVIGATION_BACKGROUND = '#18395b'


class Controller(threading.Thread):
    def __init__(self, status_frame):
        threading.Thread.__init__(self)
        self.daemon = True
        self.status_frame = status_frame

    def run(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_receive
        client.on_disconnect = self.on_disconnect
        client.connect(Config.Config.HIVEMQ_BROKER, 1883, keepalive=5)
        client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        self.status_frame.set_connection_status('Connected')

    def on_disconnect(self, client, userdata, rc):
        self.status_frame.set_connection_status('Disconnected')

    def on_receive(self, client, userdata, message):
        print('Received')


class FixedSizeLabel(tk.Frame):
    def __init__(self, parent, width, height, *args, **kwargs):
        tk.Frame.__init__(self, parent, width=width, height=height)
        self.pack_propagate(False)
        self.label = tk.Label(self, *args, **kwargs)
        self.label.pack(fill=tk.BOTH, expand=1)


class DisplayFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background='#3c3f41', height=200, width=200)
        self.navigation_frame = NavigationFrame(self)
        self.content_frame = ContentFrame(self)
        self.status_frame = StatusFrame(self)
        self.navigation_frame.grid(row=1, column=0, rowspan=1, columnspan=1, sticky='news')
        self.content_frame.grid(row=1, column=1, rowspan=1, columnspan=1, sticky='news')
        self.status_frame.grid(row=0, column=0, rowspan=1, columnspan=2, sticky='news')
        self.summary_frame = SummaryFrame(self)
        self.add_content('Summary', self.summary_frame)
        self.network_frame = NetworkFrame(self)
        self.add_content('Network', self.network_frame)
        self.weather_frame = WeatherFrame(self)
        self.add_content('Weather', self.weather_frame)
        self.pack()

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


class NetworkFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=DEFAULT_COLOR_CONTENT_BACKGROUND, height=600, width=900)


class WeatherFrame(tk.Frame):
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
    c = Controller(d.status_frame)
    c.start()

    tk.mainloop()
