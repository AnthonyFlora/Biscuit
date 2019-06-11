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
  python3 ${DIRECTORY}/Services/DefibrillatorService.py &
fi

if [ $HOST = "gateway1" ]; then
  python3 ${DIRECTORY}/Services/GatewayService.py &
  python3 ${DIRECTORY}/Services/DefibrillatorService.py &
fi

if [ $HOST = "gateway2" ]; then
  python3 ${DIRECTORY}/Services/GatewayService.py &
  python3 ${DIRECTORY}/Services/DefibrillatorService.py &
fi

if [ $HOST = "gateway3" ]; then
  python3 ${DIRECTORY}/Services/GatewayService.py &
  python3 ${DIRECTORY}/Services/DefibrillatorService.py &
fi

if [ $HOST = "gateway4" ]; then
  python3 ${DIRECTORY}/Services/GatewayService.py &
  python3 ${DIRECTORY}/Services/DefibrillatorService.py &
fi


if [ $HOST = "hyperion" ]; then
  python3 ${DIRECTORY}/Services/DisplayService.py &
  python3 ${DIRECTORY}/Services/GatewayService.py &
fi

python3 ${DIRECTORY}/Services/SystemService.py &
python3 ${DIRECTORY}/Services/HeartbeatService.py &


