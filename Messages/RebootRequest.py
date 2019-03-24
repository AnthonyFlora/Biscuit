import json


class RebootRequest:
    def __init__(self):
        self.hostname = ''

    def from_dict(self, dict_data):
        self.hostname = dict_data['hostname']

    def from_json(self, json_data):
        dict_data = json.loads(json_data)
        self.from_dict(dict_data)

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__)
