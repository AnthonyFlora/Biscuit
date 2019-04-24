#! /bin/bash

HOST=`hostname -s`
DIRECTORY=`dirname $0`
cd ${DIRECTORY}
export PYTHONPATH=${DIRECTORY}

if [ $HOST = "Anthonys-MacBook-Pro" ]; then
  echo $HOST
fi

if [ $HOST = "gateway" ]; then
  python3 ${DIRECTORY}/Services/GatewayService.py &
  python3 ${DIRECTORY}/Services/DeadmanSwitchService.py &
fi

if [ $HOST = "hyperion" ]; then
  python3 ${DIRECTORY}/Services/GatewayService.py root@192.168.11.1 &
fi

python3 ${DIRECTORY}/Services/SystemService.py &
python3 ${DIRECTORY}/Services/HeartbeatService.py &


