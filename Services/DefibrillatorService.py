import Services.Service
import collections
import time

class DefibrillatorService(Services.Service.Service):
    def __init__(self):
        Services.Service.Service.__init__(self, 'DefibrillatorService')


if __name__ == '__main__':

    retry_sleep = 10.0
    fail_thresh = 6
    start_times = collections.deque(maxlen=fail_thresh)
    for i in range(fail_thresh):
        start_times.append(0)

    while True:
        start_times.append(time.time())
        try:
            component = DefibrillatorService()
            component.run()
        except:
            None
        if start_times[fail_thresh - 1] - start_times[0]  < retry_sleep * (fail_thresh + .5):
            component = DefibrillatorService()
            component.reboot()
        print('Restarting HeartbeatService..')
        time.sleep(retry_sleep)
