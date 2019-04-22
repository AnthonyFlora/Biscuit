import Services.Service
import time

class HeartbeatService(Services.Service.Service):
    def __init__(self):
        Services.Service.Service.__init__(self, 'HeartbeatService')

    def run(self):
        self.client.loop_start()
        time.sleep(30.0)
        while self.client.is_connected:
            self.send_service_status()
            time.sleep(10.0)


if __name__ == '__main__':
    while True:
        try:
            component = HeartbeatService()
            component.run()
        except:
            None
        print('Restarting HeartbeatService..')
        time.sleep(10.0)
