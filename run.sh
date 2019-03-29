#! /bin/bash

export PYTHONPATH=${PWD}
python3 Services/SystemService.py &
python3 Services/GatewayService.py &
