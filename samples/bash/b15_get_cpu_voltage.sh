#!/bin/bash

### ラズパイのCPUのコアの電圧

VOLTS=`vcgencmd measure_volts`
VOLTS_5=${VOLTS:5}

echo "CPU core voltage is $VOLTS_5"
