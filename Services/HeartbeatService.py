import Services.Service
import time

class HeartbeatService(Services.Service.Service):
    def __init__(self):
        Services.Service.Service.__init__(self, 'HeartbeatService')

    def run(self):
        self.set_service_status('OPERATIONAL')
        while True:
            time.sleep(30)
            self.send_service_status()


if __name__ == '__main__':
    while True:
        try:
            component = HeartbeatService()
            component.run()
        except:
            print('Restarting HeartbeatService..')
            time.sleep(10.0)
