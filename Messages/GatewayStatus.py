import collections
import json
import time


class SurveyStatus:
    def __init__(self):
        self.access_point = ''
        self.download = ''
        self.upload = ''
        self.ping = ''
        self.last_update = ''

    def from_dict(self, dict_data):
        if 'access_point' in dict_data:
            self.access_point = str(dict_data['access_point'])
        self.download = str(dict_data['download'])
        self.upload = str(dict_data['upload'])
        self.ping = str(dict_data['ping'])
        if 'last_update' in dict_data:
            self.last_update = str(dict_data['last_update'])
        else:
            self.last_update = '%0.6f' % time.time()

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, sort_keys=True)


class GatewayStatus:
    def __init__(self):
        self.hostname = ''
        self.gateway_name = ''
        self.access_point = ''
        self.status = ''
        self.last_update = ''
        self.utilization = ''
        self.survey_status = collections.defaultdict(lambda: SurveyStatus())

    def from_dict(self, dict_data):
        self.hostname = dict_data['hostname']
        self.gateway_name = dict_data['gateway_name']
        self.access_point = dict_data['access_point']
        self.status = dict_data['status']
        self.last_update = dict_data['last_update']
        self.utilization = dict_data['utilization']
        for k, v in dict_data['survey_status'].items():
            self.survey_status[k].from_dict(v)
        self.last_update = '%0.6f' % time.time()

    def from_json(self, json_data):
        dict_data = json.loads(json_data)
        self.from_dict(dict_data)

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, sort_keys=True)

if __name__ == '__main__':
    g = GatewayStatus()
    x = g.to_json()
    y = GatewayStatus()
    y.from_json(x)
