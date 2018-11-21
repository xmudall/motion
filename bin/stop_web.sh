#!/bin/bash

pidfile=/tmp/flask.pid

if [  -f "$pidfile" ]; then
    pid=`cat $pidfile`
    echo "kill " $pid
    kill $pid
    rm $pidfile
else
    echo $pidfile not exist
fi