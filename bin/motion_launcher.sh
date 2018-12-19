#!/bin/bash

BIN_HOME=$(cd "$(dirname "$0")"; pwd)

nohup $BIN_HOME/motion_watchdog.sh > /dev/null 2>&1 &


