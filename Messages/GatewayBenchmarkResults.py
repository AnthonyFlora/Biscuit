import json


class GatewayBenchmarkResults:
    def __init__(self, hostname):
        self.hostname = hostname
        self.download_speed = ''
        self.upload_speed = ''
        self.ping = ''

    def from_dict(self, dict_data):
        self.download_speed = str(dict_data['download'])
        self.upload_speed = str(dict_data['upload'])
        self.ping = str(dict_data['ping'])

    def from_json(self, json_data):
        dict_data = json.loads(json_data)
        self.from_dict(dict_data)

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, sort_keys=True)

