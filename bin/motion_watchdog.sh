#!/bin/bash

BIN_HOME=$(cd "$(dirname "$0")"; pwd)

while [ true ]
do
    ps -aux | grep "python" | grep "motion.py"
    if [ $? -ne 0 ]
    then 
        echo "motion is not running, start motion ..."
	sleep 1s
        $BIN_HOME/start_all.sh
    else
	echo "motion is running!"
    fi
    sleep 2s
done


