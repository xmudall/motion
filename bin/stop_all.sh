#!/bin/bash

BIN_HOME=$(cd "$(dirname "$0")"; pwd)
$BIN_HOME/stop_motion.sh
$BIN_HOME/stop_serial.sh
$BIN_HOME/stop_snap.sh
$BIN_HOME/stop_web.sh
