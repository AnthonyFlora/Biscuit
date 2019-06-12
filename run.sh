#! /bin/bash

# gateway  00:c0:ca:96:db:a6
# gateway2 00:c0:ca:97:1a:e3
# gateway3 00:c0:ca:97:b3:11
# gateway4 00:c0:ca:97:b7:87


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
  python3 ${DIRECTORY}/Services/DisplayService.py &
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


