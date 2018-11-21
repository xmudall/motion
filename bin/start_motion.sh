#!/bin/bash

BIN_HOME=$(cd "$(dirname "$0")"; pwd)
EXEC=$BIN_HOME/../src/motion.py
sub=`date +%Y%m%d`
pidfile=/tmp/motion.pid
logfile=/tmp/log/motion_$sub.log

p3

nohup python $EXEC 2>&1 > $logfile & pid=$!

echo "process motion pid "$pid" write to "$pidfile
echo $pid > $pidfile