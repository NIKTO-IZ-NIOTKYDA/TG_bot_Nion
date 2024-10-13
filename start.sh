#!/usr/bin/bash

clear

echo "Setup env . . ."; source .venv/bin/activate && source .env

WORK_DIR=${BASH_SOURCE/"/start.sh"/"/"}

echo "# cd $WORK_DIR"; cd "$WORK_DIR"

#echo "-> Starting bot"; python3 main.py &
PID_BOT=$!;

echo "-> Starting backend"; python3 init_webapp.py &
PID_WEBAPP_BACKEND=$!;


#echo "PID BOT: $PID_BOT"
echo "PID WEBAPP BACKEND: $PID_WEBAPP_BACKEND"


trap 'kill -2 $PID_BOT $PID_WEBAPP_BACKEND; exit(0)' ERR


while : ; do sleep 1; done
