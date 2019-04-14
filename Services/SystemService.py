import Services.Service
import Messages.SystemRebootRequest
import Messages.SystemUpdateRequest
import subprocess
import time

class SystemService(Services.Service.Service):
    def __init__(self):
        Services.Service.Service.__init__(self, 'SystemService')
        self.setup_handler('/biscuit/Messages/SystemRebootRequest', self.on_receive_system_reboot_request)
        self.setup_handler('/biscuit/Messages/SystemUpdateRequest', self.on_receive_system_update_request)

    def on_receive_system_reboot_request(self, message):
        m = Messages.SystemRebootRequest.SystemRebootRequest()
        m.from_json(message.payload)
        if m.hostname == self.hostname:
            self.reboot()

    def on_receive_system_update_request(self, message):
        m = Messages.SystemUpdateRequest.SystemUpdateRequest()
        m.from_json(message.payload)
        self.set_service_status('Received myHost=%s msgHost=%s' % (self.hostname, m.hostname))
        if m.hostname == self.hostname:
            self.set_service_status('UPDATING')
            subprocess.check_output('git pull', shell=True)
            self.reboot()


if __name__ == '__main__':
    while True:
        try:
            component = SystemService()
            component.run()
        except:
            print('Restarting SystemService..')
            time.sleep(10.0)
