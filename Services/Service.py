import Messages.SystemRebootRequest
import Messages.SystemUpdateRequest
import Messages.ServiceStatus
import paho.mqtt.client as mqtt
import datetime
import subprocess
import time
import collections


class Service:
    def __init__(self, service_name='Core'):
        self.hostname = self.get_hostname()
        self.service_name = service_name
        self.client = mqtt.Client()
        self.setup_last_will()
        self.connect_to_broker()
        self.handlers = collections.defaultdict(lambda: self.on_receive_default)

    def setup_last_will(self):
        self.service_status_topic = '/biscuit/Statuses/' + self.hostname + '/' + self.service_name
        self.service_state = Messages.ServiceStatus.ServiceStatus()
        self.service_state.hostname = self.hostname
        self.service_state.service = self.service_name
        self.service_state.version = '20190605_0938p'
        self.service_state.status = 'OFFLINE'
        self.client.will_set(self.service_status_topic, self.service_state.to_json(), qos=1, retain=True)

    def setup_handler(self, topic, handler):
        self.handlers[topic] = handler
        self.client.subscribe(topic, qos=1)

    def connect_to_broker(self):
        self.client.is_connected = False
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_receive
        self.client.on_disconnect = self.on_disconnect
        self.client.connect('broker.hivemq.com', 1883) # TODO move to config

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.client.is_connected = True
            self.set_service_status('OPERATIONAL')
        else:
            self.client.loop_stop()
            raise Exception('MQTT Connection Failed')

    def on_disconnect(self, client, userdata, rc):
        print('Disconnected')
        self.client.is_connected = False
        self.client.disconnect()
        self.client.loop_stop()

    def on_receive(self, client, userdata, message):
        handler = self.handlers[message.topic]
        handler(message.payload.decode("utf-8"))
        for topic,handler in self.handlers.items():
            if '#' in topic:
                wild_topic = topic.replace('#', '')
                if wild_topic in message.topic:
                    handler(message.payload.decode("utf-8"))

    def on_receive_default(self, message):
        None

    def run(self):
        self.client.loop_forever()

    def get_hostname(self):
        return subprocess.check_output('hostname -s 2>/dev/null', shell=True).decode('utf-8').split().pop()

    def set_service_status(self, status):
        self.service_state.status = status
        self.send_service_status()

    def send_service_status(self):
        self.service_state.last_update = str(datetime.datetime.now())
        ret = self.client.publish(self.service_status_topic, self.service_state.to_json(), qos=1, retain=True)
        if ret.rc != 0:  # TODO this should be in a general send, not just status, is it needed though, will disc be detect?
            print('Could not publish')
            self.client.disconnect()

    def reboot(self):
        self.set_service_status('SHUTTING DOWN')
        self.client.loop_stop()
        self.client.disconnect()
        return subprocess.check_output('sudo reboot', shell=True)


if __name__ == '__main__':
    while True:
        try:
            component = Service()
            component.run()
        except:
            print(str(datetime.datetime.now()), 'Restarting Service..')
            time.sleep(10.0)
