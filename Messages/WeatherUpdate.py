import json


class WeatherUpdate:
    def __init__(self):
        self.sensor_id = ''
        self.temperature = ''
        self.humidity = ''

    def from_dict(self, dict_data):
        self.sensor_id = dict_data['sensor_id']
        self.temperature = dict_data['temperature']
        self.humidity = dict_data['humidity']

    def from_json(self, json_data):
        dict_data = json.loads(json_data)
        self.from_dict(dict_data)

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, sort_keys=True)

    def __repr__(self):
        return str(self.__dict__)
