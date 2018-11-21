#!/bin/bash

BIN_HOME=$(cd "$(dirname "$0")"; pwd)
cd $BIN_HOME/../src
export FLASK_APP=web.app
sub=`date +%Y%m%d`
pidfile=/tmp/flask.pid
logfile=/tmp/log/flask_$sub.log
if [ ! -d /tmp/log ]; then
    mkdir /tmp/log
fi

source /home/pi/env/p3/bin/activate

nohup python -m flask run 2>&1 > $logfile & pid=$!

echo "process flask pid "$pid" write to "$pidfile
echo $pid > $pidfile