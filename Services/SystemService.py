import Messages.RebootRequest
import Messages.ServiceStatus
import paho.mqtt.client as mqtt
import datetime
import subprocess
import time

class SystemController:
    def __init__(self):
        self.hostname = self.get_hostname()
        self.status_topic = '/biscuit/Statuses/' + self.hostname + '/SystemController'
        self.state = Messages.ServiceStatus.ServiceStatus()
        self.state.hostname = self.hostname
        self.state.status = 'OFFLINE'
        self.client = mqtt.Client()
        self.client.will_set(self.status_topic, self.state.to_json(), qos=0, retain=True)
        self.connect_to_broker()

    def connect_to_broker(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_receive
        self.client.connect('iot.eclipse.org', 1883)
        self.client.subscribe('/biscuit/Messages/RebootRequest')

    def on_connect(self, client, userdata, flags, rc):
        self.set_service_status('OPERATIONAL')

    def on_receive(self, client, userdata, message):
        if '/biscuit/Messages/RebootRequest' in message.topic:
            self.on_receive_reboot_request(message)
        else:
            self.on_receive_default(message)

    def on_receive_reboot_request(self, message):
        m = Messages.RebootRequest.RebootRequest()
        m.from_json(message.payload)
        if m.hostname == self.hostname:
            self.set_service_status('SHUTTING DOWN')
            self.client.loop_stop()
            self.client.disconnect()
            return subprocess.check_output('reboot', shell=True)

    def on_receive_default(self, message):
        print('received default', message.topic)

    def run(self):
        self.client.loop_forever()

    def get_hostname(self):
        return subprocess.check_output('hostname -s 2>/dev/null', shell=True).decode('utf-8').split().pop()

    def set_service_status(self, status):
        self.state.status = status
        self.send_service_status()

    def send_service_status(self):
        self.state.last_update = str(datetime.datetime.now())
        self.client.publish(self.status_topic, self.state.to_json(), qos=0, retain=True)


if __name__ == '__main__':
    while True:
        component = SystemController()
        component.run()
        time.sleep(10.0)
