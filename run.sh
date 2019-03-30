#! /bin/bash


DIRECTORY=`dirname $0`
cd ${DIRECTORY}
export PYTHONPATH=${DIRECTORY}
python3 ${DIRECTORY}/Services/SystemService.py &
python3 ${DIRECTORY}/Services/GatewayService.py &