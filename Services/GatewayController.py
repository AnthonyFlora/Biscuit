import Messages.GatewayStatus
import paho.mqtt.client as mqtt
import datetime
import subprocess
import time

class GatewayController:
    def __init__(self, remote):
        self.remote = remote
        self.hostname = self.get_hostname()
        self.status_topic = '/biscuit/gateway_status/' + self.hostname
        self.state = Messages.GatewayStatus.GatewayStatus()
        self.state.gateway_name = self.hostname
        self.state.status = 'OFFLINE'
        self.client = mqtt.Client()
        self.client.will_set(self.status_topic, self.state.to_json(), qos=1, retain=True)
        self.connect_to_broker()

    def connect_to_broker(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_receive
        self.client.connect('iot.eclipse.org', 1883)
        self.client.subscribe('/biscuit/gateway_status_request')
        self.client.subscribe('/biscuit/gateway_reboot_request')

    def on_connect(self, client, userdata, flags, rc):
        self.set_status('OPERATIONAL')
        self.update_status()

    def on_receive(self, client, userdata, message):
        if '/biscuit/gateway_status_request' in message.topic:
            self.on_receive_gateway_status_request(message)
        elif '/biscuit/gateway_reboot_request' in message.topic:
            self.on_receive_gateway_status_request(message)
        else:
            self.on_receive_default(message)

    def on_receive_default(self, message):
        print('received default', message.topic)

    def on_receive_gateway_status_request(self, message):
        self.update_status()

    def on_receive_gateway_reboot_request(self, message):
        print('received gateway reboot request', message.topic)

    def run(self):
        self.client.loop_forever()

    def get_hostname(self):
        return subprocess.check_output('ssh %s hostname 2>/dev/null' % (self.remote), shell=True).decode('utf-8').split().pop()

    def get_access_point_address(self):
        access_point_address = subprocess.check_output('ssh %s iwconfig 2>/dev/null | grep Access' % (self.remote), shell=True)
        access_point_address = access_point_address.decode('utf-8').split().pop()
        return access_point_address

    def set_status(self, status):
        self.state.status = status
        self.send_gateway_status()

    def update_status(self):
        self.state.access_point_address = self.get_access_point_address()
        self.send_gateway_status()

    def send_gateway_status(self):
        self.state.last_update = str(datetime.datetime.now())
        self.client.publish(self.status_topic, self.state.to_json())


if __name__ == '__main__':
    while True:
        component = GatewayController('root@192.168.11.1')
        component.run()
        time.sleep(10.0)
