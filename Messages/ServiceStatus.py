import json


class ServiceStatus:
    def __init__(self):
        self.hostname = ''
        self.service = ''
        self.status = ''
        self.version = ''

    def from_dict(self, dict_data):
        self.hostname = dict_data['hostname']
        self.service = dict_data['service']
        self.status = dict_data['status']
        self.version = dict_data['version']

    def from_json(self, json_data):
        dict_data = json.loads(json_data)
        self.from_dict(dict_data)

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, sort_keys=True)

