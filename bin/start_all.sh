#!/bin/bash

BIN_HOME=$(cd "$(dirname "$0")"; pwd)
$BIN_HOME/start_motion.sh
$BIN_HOME/start_serial.sh
$BIN_HOME/start_web.sh
