import json


class GatewayBenchmarkResults:
    def __init__(self):
        self.hostname = ''
        self.download_speed = ''
        self.upload_speed = ''
        self.ping = ''

    def from_dict(self, dict_data):
        self.hostname = dict_data['hostname']
        self.download_speed = dict_data['download']
        self.upload_speed = dict_data['upload']
        self.ping = dict_data['ping']

    def from_json(self, json_data):
        dict_data = json.loads(json_data)
        self.from_dict(dict_data)

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, sort_keys=True)

