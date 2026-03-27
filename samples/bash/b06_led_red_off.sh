#!/bin/bash

### 赤いLEDを消灯する

LED_ON=dh
LED_OFF=dl

LED_RED=16
LED_GREEN=20
LED_BLUE=21

echo "LED RED OFF."
/usr/bin/pinctrl $LED_RED op $LED_OFF
