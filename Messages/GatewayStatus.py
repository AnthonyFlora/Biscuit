import json
import collections


class GatewayStatus:
    def __init__(self):
        self.gateway_name = ''
        self.access_point_address = ''
        self.status = ''
        self.last_update = ''
        self.utilization = ''
        self.survey_status = collections.defaultdict(lambda: SurveyStatus())

    def from_dict(self, dict_data):
        self.gateway_name = dict_data['gateway_name']
        self.access_point_address = dict_data['access_point_address']
        self.status = dict_data['status']
        self.last_update = dict_data['last_update']
        self.utilization = dict_data['utilization']
        for k, v in dict_data['survey_status'].items():
            self.survey_status[k].from_dict(v)

    def from_json(self, json_data):
        dict_data = json.loads(json_data)
        self.from_dict(dict_data)

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__)

