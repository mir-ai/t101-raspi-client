#!/bin/bash

### バッテリー低電圧ボタンが押されたかを監視する

echo "Watching DOOR OPEN button..."
echo
echo "* Press ctrl-c to exit."

PIN_DOOR_OPEN=11

/usr/bin/pinctrl -e set $PIN_DOOR_OPEN ip pu  > /dev/null 2>&1

while true
do
    RES=`/usr/bin/pinctrl get $PIN_DOOR_OPEN | grep hi`
    if [ -n "$RES" ]
    then
        echo "OFF"
    else
        echo "ON"
    fi
    sleep 1
done

