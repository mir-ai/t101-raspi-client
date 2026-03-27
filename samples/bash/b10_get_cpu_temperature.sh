#!/bin/bash

### CPUの温度を返す

CPU_TEMP=`/bin/cat /sys/class/thermal/thermal_zone0/temp | awk '{print $1/1000}'`

echo "CPU core temperature is $CPU_TEMP"
