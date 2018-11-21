#!/bin/bash

BIN_HOME=$(cd "$(dirname "$0")"; pwd)
EXEC=$BIN_HOME/../src/snap.py
sub=`date +%Y%m%d`
pidfile=/tmp/snap.pid
logfile=/tmp/log/snap_$sub.log
if [ ! -d /tmp/log ]; then
    mkdir /tmp/log
fi

source /home/pi/env/p3/bin/activate

nohup python $EXEC 2>&1 > $logfile & pid=$!

echo "process snap pid "$pid" write to "$pidfile
echo $pid > $pidfile