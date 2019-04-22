import Services.Service
import time

class HeartbeatService(Services.Service.Service):
    def __init__(self):
        Services.Service.Service.__init__(self, 'HeartbeatService')

    def run(self):
        self.client.loop_start()
        while True:
            time.sleep(60.0)
            self.send_service_status()


if __name__ == '__main__':
    while True:
        try:
            component = HeartbeatService()
            component.run()
        except:
            print('Restarting HeartbeatService..')
            time.sleep(10.0)
