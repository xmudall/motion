#!/bin/bash

BIN_HOME=$(cd "$(dirname "$0")"; pwd)
EXEC=$BIN_HOME/../src/serial_out.py
sub=`date +%Y%m%d`
pidfile=/tmp/serial.pid
logfile=/tmp/log/serial_$sub.log
if [ ! -d /tmp/log ]; then
    mkdir /tmp/log
fi

source /home/pi/env/p3/bin/activate

nohup python $EXEC 2>&1 > $logfile & pid=$!

echo "process serial pid "$pid" write to "$pidfile
echo $pid > $pidfile