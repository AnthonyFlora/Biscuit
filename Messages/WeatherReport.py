import json

import collections
import datetime
import Messages.WeatherUpdate

class WeatherReport:
    def __init__(self):
        self.last_update = ''
        self.weather_updates = collections.defaultdict(lambda: Messages.WeatherUpdate.WeatherUpdate())

    def from_dict(self, dict_data):
        self.last_update = dict_data['last_update']
        for k, v in dict_data['weather_updates'].items():
            self.weather_updates[k].from_dict(v)

    def from_json(self, json_data):
        dict_data = json.loads(json_data)
        self.from_dict(dict_data)

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, sort_keys=True)

    def __repr__(self):
        o = str(self.__class__) + '\n'
        o = o + '  last_update = %0.6f (%s)\n' % (self.last_update, datetime.datetime.fromtimestamp(self.last_update).strftime('%Y-%m-%d %H:%M:%S'))
        for k,v in self.weather_updates.items():
          o = o + '  weather_updates[%s] = %s\n' % (k, v)
        return o

