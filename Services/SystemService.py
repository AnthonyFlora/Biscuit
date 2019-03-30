import Messages.SystemRebootRequest
import Messages.SystemUpdateRequest
import Messages.ServiceStatus
import paho.mqtt.client as mqtt
import datetime
import subprocess
import time

class SystemService:
    def __init__(self):
        self.hostname = self.get_hostname()
        self.status_topic = '/biscuit/Statuses/' + self.hostname + '/SystemService'
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
        self.client.subscribe('/biscuit/Messages/SystemRebootRequest')
        self.client.subscribe('/biscuit/Messages/SystemUpdateRequest')

    def on_connect(self, client, userdata, flags, rc):
        self.set_service_status('OPERATIONAL')

    def on_receive(self, client, userdata, message):
        print(message.topic)
        if '/biscuit/Messages/SystemRebootRequest' in message.topic:
            message.payload = message.payload.decode("utf-8")
            self.on_receive_system_reboot_request(message)
        elif '/biscuit/Messages/SystemUpdateRequest' in message.topic:
            message.payload = message.payload.decode("utf-8")
            self.on_receive_system_update_request(message)
        else:
            self.on_receive_default(message)

    def on_receive_system_reboot_request(self, message):
        m = Messages.SystemRebootRequest.SystemRebootRequest()
        m.from_json(message.payload)
        if m.hostname == self.hostname:
            self.set_service_status('SHUTTING DOWN')
            self.client.loop_stop()
            self.client.disconnect()
            return subprocess.check_output('reboot', shell=True)

    def on_receive_system_update_request(self, message):
        m = Messages.SystemUpdateRequest.SystemUpdateRequest()
        m.from_json(message.payload)
        print(m.hostname, self.hostname)
        if m.hostname == self.hostname:
            self.set_service_status('UPDATING')
            subprocess.check_output('git pull', shell=True)
            self.set_service_status('SHUTTING DOWN')
            self.client.loop_stop()
            self.client.disconnect()
            return subprocess.check_output('sudo reboot', shell=True)

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
        try:
            component = SystemService()
            component.run()
            time.sleep(10.0)
        except:
            print('Restarting SystemService..')
