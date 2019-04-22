import json


class SurveyStatus:
    def __init__(self):
        self.x = ''
        self.y = ''

    def from_dict(self, dict_data):
        self.x = dict_data['x']
        self.y = dict_data['y']

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, sort_keys=True)