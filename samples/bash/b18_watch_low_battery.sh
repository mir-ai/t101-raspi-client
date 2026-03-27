#!/bin/bash

### バッテリー低電圧ボタンが押されたかを監視する

echo "Watching LOW BATTERY button..."
echo
echo "* Press ctrl-c to exit."

PIN_LOW_BATT=9

/usr/bin/pinctrl -e set $PIN_LOW_BATT ip pu  > /dev/null 2>&1

while true
do
    RES=`/usr/bin/pinctrl get $PIN_LOW_BATT | grep hi`
    if [ -n "$RES" ]
    then
        echo "OFF"
    else
        echo "ON"
    fi
    sleep 1
done

