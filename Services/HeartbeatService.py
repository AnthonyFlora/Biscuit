import Services.Service
import time

class HeartbeatService(Services.Service.Service):
    def __init__(self):
        Services.Service.Service.__init__(self, 'HeartbeatService')
        self.heartbeat_periodic = 5 * 60

    def run(self):
        self.client.loop_start()
        time.sleep(self.heartbeat_periodic)
        while self.client.is_connected:
            self.send_service_status()
            time.sleep(self.heartbeat_periodic)


if __name__ == '__main__':
    while True:
        try:
            component = HeartbeatService()
            component.run()
        except:
            None
        print('Restarting HeartbeatService..')
        time.sleep(10.0)
