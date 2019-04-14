import Services.Service
import Messages.SystemRebootRequest
import Messages.SystemUpdateRequest
import subprocess
import time

class SystemService(Services.Service.Service):
    def __init__(self):
        Services.Service.Service.__init__(self, 'SystemService')
        self.handlers['/biscuit/Messages/SystemRebootRequest'] = self.on_receive_system_reboot_request
        self.handlers['/biscuit/Messages/SystemUpdateRequest'] = self.on_receive_system_update_request

    def on_receive_system_reboot_request(self, message):
        m = Messages.SystemRebootRequest.SystemRebootRequest()
        m.from_json(message.payload)
        if m.hostname == self.hostname:
            self.set_service_status('SHUTTING DOWN')
            self.client.loop_stop()
            self.client.disconnect()
            return subprocess.check_output('sudo reboot', shell=True)

    def on_receive_system_update_request(self, message):
        m = Messages.SystemUpdateRequest.SystemUpdateRequest()
        m.from_json(message.payload)
        if m.hostname == self.hostname:
            self.set_service_status('UPDATING')
            subprocess.check_output('git pull', shell=True)
            self.set_service_status('SHUTTING DOWN')
            self.client.loop_stop()
            self.client.disconnect()
            return subprocess.check_output('sudo reboot', shell=True)


if __name__ == '__main__':
    while True:
        try:
            component = SystemService()
            component.run()
        except:
            print('Restarting SystemService..')
            time.sleep(10.0)
