import Services.Service
import Messages.GatewayBenchmarkRequest
import Messages.GatewayBenchmarkResults
import Messages.GatewayStatus
import Messages.GatewayStatusRequest
import Messages.SystemRebootRequest
import Messages.SystemUpdateRequest
import Messages.ServiceStatus
import datetime
import time
import subprocess


class GatewayService(Services.Service.Service):
    def __init__(self):
        Services.Service.Service.__init__(self, 'GatewayService')
        self.gateway_status = Messages.GatewayStatus.GatewayStatus()
        self.gateway_status.hostname = self.hostname
        self.gateway_status_topic = '/biscuit/Messages/GatewayStatus'
        self.update_gateway_status()
        self.update_benchmark_results()
        self.setup_handler('/biscuit/Messages/GatewayBenchmarkRequest', self.on_receive_gateway_benchmark_request)
        self.setup_handler('/biscuit/Messages/GatewayStatusRequest', self.on_receive_gateway_status_request)

    def on_receive_gateway_status_request(self, message):
        m = Messages.GatewayStatusRequest.GatewayStatusRequest()
        m.from_json(message)
        if m.hostname == self.hostname:
            self.update_gateway_status()
            self.send_gateway_status()

    def on_receive_gateway_benchmark_request(self, message):
        m = Messages.GatewayBenchmarkRequest.GatewayBenchmarkRequest()
        m.from_json(message)
        if m.hostname == self.hostname:
            if m.refresh:
                self.update_benchmark_results()
            else:
                self.send_gateway_status()

    def send_gateway_status(self):
        self.client.publish(self.gateway_status_topic, self.gateway_status.to_json(), qos=1)

    def update_gateway_status(self):
        self.gateway_status.access_point = self.get_access_point_address()

    def get_access_point_address(self):
        cmd = 'iwconfig 2>/dev/null | grep Access | grep -v Not-Associated'
        ret = ''
        try:
            access_point_address = subprocess.check_output(cmd, shell=True)
            access_point_address = access_point_address.decode('utf-8').split().pop()
            ret = access_point_address
        except:
            None
        return ret

    def get_benchmark_results(self):
        cmd = 'speedtest-cli --json 2>/dev/null'
        benchmark_json = subprocess.check_output(cmd, shell=True)
        benchmark_json = benchmark_json.decode('utf-8')
        return benchmark_json

    def update_benchmark_results(self):
        self.client.publish('/biscuit/debug', 'Getting AP', qos=1)
        access_point = self.get_access_point_address()
        self.client.publish('/biscuit/debug', 'Getting BM', qos=1)
        benchmark_json = self.get_benchmark_results()
        self.client.publish('/biscuit/debug', 'Setting MSG', qos=1)
        self.gateway_status.survey_status[access_point].from_json(benchmark_json)
        self.gateway_status.survey_status[access_point].last_update = time.time()




if __name__ == '__main__':
    while True:
        try:
            component = GatewayService()
            component.run()
        except:
            None
        print(str(datetime.datetime.now()), 'Restarting GatewayService..')
        time.sleep(10.0)
