import collections
import Config.Config
import Services.Service
import Messages.WeatherUpdate
import Messages.WeatherReport
import time

class WeatherService(Services.Service.Service):
    def __init__(self):
        Services.Service.Service.__init__(self, 'WeatherService', broker=Config.Config.HYPERION_BROKER)
        self.weather_report_topic = '/biscuit/Messages/WeatherReport'
        self.sensor_to_room = collections.defaultdict()
        self.sensor_to_room['sensor001'] = 'office'
        self.sensor_to_room['sensor002'] = 'master'
        self.sensor_to_room['sensor003'] = 'basement'
        self.sensor_to_room['sensor004'] = 'family'
        self.sensor_to_room['sensor005'] = 'guest'
        self.weather_report = Messages.WeatherReport.WeatherReport()
        self.weather_report.last_update = time.time()
        self.weather_report.weather_updates['office'].temperature = 0.0
        self.weather_report.weather_updates['master'].temperature = 0.0
        self.weather_report.weather_updates['basement'].temperature = 0.0
        self.weather_report.weather_updates['family'].temperature = 0.0
        self.weather_report.weather_updates['guest'].temperature = 0.0
        self.setup_handler('/biscuit/SensorMessages/WeatherUpdate', self.on_receive_system_weather_update)

    def time_since_last_send(self):
        return time.time() - self.weather_report.last_update

    def on_receive_system_weather_update(self, message):
        m = Messages.WeatherUpdate.WeatherUpdate()
        m.from_json(message.replace('\'', '\"')) # sensor using ' not ", fix here until sensor does
        is_initial_data = self.weather_report.weather_updates[self.sensor_to_room[m.sensor_id]].temperature == 0.0
        self.weather_report.weather_updates[self.sensor_to_room[m.sensor_id]].sensor_id = m.sensor_id
        self.weather_report.weather_updates[self.sensor_to_room[m.sensor_id]].temperature = m.temperature
        self.weather_report.weather_updates[self.sensor_to_room[m.sensor_id]].humidity = m.humidity
        if is_initial_data or self.time_since_last_send() > 300:
            self.send_weather_report()

    def send_weather_report(self):
        self.weather_report.last_update = time.time()
        self.client.publish(self.weather_report_topic, self.weather_report.to_json(), qos=1, retain=True)
        print('sent report %s' % str(self.weather_report))


if __name__ == '__main__':
    while True:
        try:
            component = WeatherService()
            component.run()
        except Exception as e:
            print(e)
        print('Restarting WeatherService..')
        time.sleep(10.0)
