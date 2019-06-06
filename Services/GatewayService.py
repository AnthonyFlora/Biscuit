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
import sys
import subprocess

class GatewayService(Services.Service.Service):
    def __init__(self, command_prefix):
        Services.Service.Service.__init__(self, 'GatewayService')
        self.command_prefix = ''
        if command_prefix:
            self.command_prefix = 'ssh ' + command_prefix + ' '
        self.gateway_status = Messages.GatewayStatus.GatewayStatus()
        self.gateway_status.hostname = self.hostname
        self.gateway_status.gateway_name = command_prefix
        self.gateway_status_topic = '/biscuit/Messages/GatewayStatus'
        self.gateway_benchmark_results = Messages.GatewayBenchmarkResults.GatewayBenchmarkResults(self.hostname)
        self.gateway_benchmark_results_topic = '/biscuit/Messages/GatewayBenchmarkResults'
        self.update_gateway_status()
        self.update_benchmark_results()
        self.setup_handler('/biscuit/Messages/GatewayBenchmarkRequest', self.on_receive_gateway_benchmark_request)
        self.setup_handler('/biscuit/Messages/GatewayRebootRequest', self.on_receive_gateway_reboot_request)
        self.setup_handler('/biscuit/Messages/GatewayStatusRequest', self.on_receive_gateway_status_request)


    def on_receive_gateway_reboot_request(self, message):
        m = Messages.GatewayRebootRequest.GatewayRebootRequest()
        m.from_json(message)
        # if m.hostname == self.hostname:
        #     self.set_service_status('SHUTTING DOWN')
        #     self.client.loop_stop()
        #     self.client.disconnect()
        #     return subprocess.check_output('reboot', shell=True)

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
                self.send_benchmark_results()

    def send_gateway_status(self):
        self.client.publish(self.gateway_status_topic, self.gateway_status.to_json(), qos=1)

    def update_gateway_status(self):
        self.gateway_status.access_point_address = self.get_access_point_address()
        self.send_gateway_status()

    def get_access_point_address(self):
        cmd = '%s iwconfig 2>/dev/null | grep Access | grep -v Not-Associated' % (self.command_prefix)
        access_point_address = subprocess.check_output(cmd, shell=True)
        access_point_address = access_point_address.decode('utf-8').split().pop()
        return access_point_address

    def get_benchmark_results(self):
        cmd = 'speedtest-cli --json 2>/dev/null'
        benchmark_json = subprocess.check_output(cmd, shell=True)
        benchmark_json = benchmark_json.decode('utf-8')
        return benchmark_json

    def update_benchmark_results(self):
        benchmark_json = self.get_benchmark_results()
        self.gateway_benchmark_results.from_json(benchmark_json)
        self.send_benchmark_results()

    def send_benchmark_results(self):
        self.client.publish(self.gateway_benchmark_results_topic, self.gateway_benchmark_results.to_json(), qos=1)




if __name__ == '__main__':
    arg_command_prefix = None
    if len(sys.argv) > 1:
        arg_command_prefix = sys.argv[1]

    while True:
        try:
            component = GatewayService(arg_command_prefix)
            component.run()
        except:
            None
        print(str(datetime.datetime.now()), 'Restarting GatewayService..')
        time.sleep(10.0)
