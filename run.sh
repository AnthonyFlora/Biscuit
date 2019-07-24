#! /bin/bash

# Gateways
#
# gateway  00:c0:ca:96:db:a6
# gateway2 00:c0:ca:97:1a:e3
# gateway3 00:c0:ca:97:b3:11
# gateway4 00:c0:ca:97:b7:87

# Connect to AP
#
# sudo iwlist wlan1 scan | grep "ESSID\|Signal\|Address" | grep -B2 xfinity
#
# sudo ip link set wlan1 down
# sudo ip addr flush dev wlan1
# sudo ip link set wlan1 up
# sudo iwconfig wlan1 essid xfinitywifi ap CE:CA:B5:EF:B5:50
#
# sudo ip link set wlan1 down; sudo ip addr flush dev wlan1; sudo ip link set wlan1 up; sudo iwconfig wlan1 essid xfinitywifi ap CE:CA:B5:EF:B5:50
#
# ifconfig

# Blacklist
# 92:AD:43:A5:3A:30

# TODO
# - Repair benchmark stats on GUI
# - Merge Defribrillator to Gateway
# - Remove Heartbeat
# - Support access point scan



HOST=`hostname -s`
DIRECTORY=`dirname $0`
cd ${DIRECTORY}
export PYTHONPATH=${DIRECTORY}

if [ $HOST = "Anthonys-MBP" ]; then
  echo $HOST
  python3 ${DIRECTORY}/Services/DisplayService.py &
  python3 ${DIRECTORY}/Services/WeatherService.py &
fi

if [ $HOST = "gateway1" ]; then
  #sudo ip link set wlan1 down; sudo ip addr flush dev wlan1; sudo ip link set wlan1 up; sudo iwconfig wlan1 essid xfinitywifi ap CE:CA:B5:EF:B5:50
  python3 ${DIRECTORY}/Services/GatewayService.py &
  python3 ${DIRECTORY}/Services/DefibrillatorService.py &
fi

if [ $HOST = "gateway2" ]; then
  #sudo ip link set wlan1 down; sudo ip addr flush dev wlan1; sudo ip link set wlan1 up; sudo iwconfig wlan1 essid xfinitywifi ap CE:CA:B5:EF:B5:50
  python3 ${DIRECTORY}/Services/GatewayService.py &
  python3 ${DIRECTORY}/Services/DefibrillatorService.py &
fi

if [ $HOST = "gateway3" ]; then
  #sudo ip link set wlan1 down; sudo ip addr flush dev wlan1; sudo ip link set wlan1 up; sudo iwconfig wlan1 essid xfinitywifi ap CE:CA:B5:EF:B5:50
  python3 ${DIRECTORY}/Services/GatewayService.py &
  python3 ${DIRECTORY}/Services/DefibrillatorService.py &
fi

if [ $HOST = "gateway4" ]; then
  #sudo ip link set wlan1 down; sudo ip addr flush dev wlan1; sudo ip link set wlan1 up; sudo iwconfig wlan1 essid xfinitywifi ap CE:CA:B5:EF:B5:50
  python3 ${DIRECTORY}/Services/GatewayService.py &
  python3 ${DIRECTORY}/Services/DefibrillatorService.py &
fi


if [ $HOST = "hyperion" ]; then
  python3 ${DIRECTORY}/Services/DisplayService.py &
  python3 ${DIRECTORY}/Services/WeatherService.py &
fi

python3 ${DIRECTORY}/Services/SystemService.py &
python3 ${DIRECTORY}/Services/HeartbeatService.py &


