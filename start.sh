#!/usr/bin/bash

echo "Setup env . . .";
source .env
source .venv/bin/activate

echo "-> Starting bot"; python3 main.py &
PID_BOT=$!;

echo "-> Starting backend"; python3 init_webapp.py &
PID_WEBAPP_BACKEND=$!;


echo "PID BOT: $PID_BOT"
echo "PID WEBAPP BACKEND: $PID_WEBAPP_BACKEND"


trap 'kill -2 $PID_BOT $PID_WEBAPP_BACKEND; exit(0)' ERR


while : ; do sleep 1; done
