import json


class SurveyStatus:
    def __init__(self):
        self.access_point_address = ''
        self.quality = ''
        self.encryption_key = ''
        self.essid = ''

    def from_dict(self, dict_data):
        self.access_point_address = dict_data['access_point_address']
        self.quality = dict_data['quality']
        self.encryption_key = dict_data['encryption_key']
        self.essid = dict_data['essid']

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, sort_keys=True)