import json
import time

class GatewayBenchmarkResults:
    def __init__(self, hostname):
        self.hostname = hostname
        self.download_speed = ''
        self.upload_speed = ''
        self.ping = ''
        self.last_update = ''

    def from_dict(self, dict_data):
        # hostname in init
        self.download_speed = str(dict_data['download'])
        self.upload_speed = str(dict_data['upload'])
        self.ping = str(dict_data['ping'])
        self.last_update = '%0.6f' % time.time()

    def from_json(self, json_data):
        dict_data = json.loads(json_data)
        self.from_dict(dict_data)

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, sort_keys=True)

