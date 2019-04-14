import Services.Service
import Messages.GatewayStatus
import Messages.SystemRebootRequest
import Messages.SystemUpdateRequest
import Messages.ServiceStatus
import paho.mqtt.client as mqtt
import datetime
import subprocess
import time
import sys

class GatewayService(Services.Service.Service):
    def __init__(self, gateway):
        Services.Service.Service.__init__(self, 'GatewayService')
        self.gateway_status = Messages.GatewayStatus.GatewayStatus()
        self.gateway_status.hostname = self.hostname
        self.gateway_status.gateway_name = gateway
        self.setup_handler('/biscuit/Messages/GatewayRebootRequest', self.on_receive_gateway_reboot_request)
        self.setup_handler('/biscuit/Messages/GatewayStatusRequest', self.on_receive_gateway_status_request)

    def on_receive_gateway_reboot_request(self, message):
        m = Messages.GatewayRebootRequest.GatewayRebootRequest()
        m.from_json(message.payload)
        print(self.hostname, 'TODO gateway reboot request')
        # if m.hostname == self.hostname:
        #     self.set_service_status('SHUTTING DOWN')
        #     self.client.loop_stop()
        #     self.client.disconnect()
        #     return subprocess.check_output('reboot', shell=True)

    def on_receive_gateway_status_request(self, message):
        m = Messages.GatewayStatusRequest.GatewayStatusRequest()
        m.from_json(message.payload)
        if m.hostname == self.hostname:
            self.send_gateway_status()

    def send_gateway_status(self):
        print(self.hostname, self.gateway_status.gateway_name, 'TODO send gateway status')
        self.client.publish(self.status_topic, self.gateway_status.to_json(), qos=1, retain=True)

if __name__ == '__main__':
    gateway = 'localhost'
    if len(sys.argv) > 1:
        gateway = sys.argv[1]

    while True:
        try:
            component = GatewayService(gateway)
            component.run()
        except:
            print('Restarting GatewayService..')
            time.sleep(10.0)
