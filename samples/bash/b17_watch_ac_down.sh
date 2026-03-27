#!/bin/bash

### AC電源断ボタンが押されたかを監視する

echo "Watching AC DOWN button..."
echo
echo "* Press ctrl-c to exit."

PIN_AC_DOWN=10

/usr/bin/pinctrl -e set $PIN_AC_DOWN ip pu  > /dev/null 2>&1

while true
do
    RES=`/usr/bin/pinctrl get $PIN_AC_DOWN | grep hi`
    if [ -n "$RES" ]
    then
        echo "OFF"
    else
        echo "ON"
    fi
    sleep 1
done

