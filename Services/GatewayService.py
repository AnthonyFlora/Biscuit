import Services.Service
import Messages.GatewayBenchmarkRequest
import Messages.GatewayStatus
import Messages.GatewayStatusRequest
import Messages.SystemRebootRequest
import Messages.SystemUpdateRequest
import Messages.ServiceStatus
import datetime
import time
import subprocess
import os


class GatewayService(Services.Service.Service):
    def __init__(self):
        Services.Service.Service.__init__(self, 'GatewayService')
        self.gateway_status = Messages.GatewayStatus.GatewayStatus()
        self.gateway_status.hostname = self.hostname
        self.gateway_status_topic = '/biscuit/Messages/GatewayStatus'
        self.update_gateway_status()
        # self.update_benchmark_results()
        # Disable initial benchmarking for now
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

    def on_receive_gateway_survey_request(self, message):
        None

    def send_gateway_status(self):
        self.client.publish(self.gateway_status_topic, self.gateway_status.to_json(), qos=1)

    def update_gateway_status(self):
        self.gateway_status.access_point = self.get_access_point_address()

    def get_access_point_address(self):
        cmd = 'iwconfig 2>/dev/null | grep -A 1 wlan1 | grep Access | grep -v Not-Associated'
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
        access_point_before = None
        access_point_after = None
        benchmark_json = None
        while (not access_point_before) or (access_point_before != access_point_after):
            access_point_before = self.get_access_point_address()
            benchmark_json = self.get_benchmark_results()
            access_point_after = self.get_access_point_address()
        self.gateway_status.survey_status[access_point_before].from_json(benchmark_json)
        self.gateway_status.survey_status[access_point_before].last_update = time.time()

if __name__ == '__main__':
    while True:
        try:
            component = GatewayService()
            component.run()
        except:
            None
        print(str(datetime.datetime.now()), 'Restarting GatewayService..')
        os.system('sudo ip link set wlan1 down; sudo ip addr flush dev wlan1; sudo ip link set wlan1 up; sudo iwconfig wlan1 essid xfinitywifi ap CE:CA:B5:EF:B5:50')
        time.sleep(10.0)
