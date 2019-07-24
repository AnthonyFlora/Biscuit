import Services.Service
import collections
import datetime
import time

class DefibrillatorService(Services.Service.Service):
    def __init__(self):
        Services.Service.Service.__init__(self, 'DefibrillatorService')


if __name__ == '__main__':

    initial_sleep = 60.0
    while True:
        try:
            time.sleep(initial_sleep)
            component = DefibrillatorService()
            component.run()
        except:
            None

        print(str(datetime.datetime.now()), 'Restarting DefibrillatorService..')

