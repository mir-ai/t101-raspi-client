#!/bin/bash

### 緑のLEDを点灯する

LED_ON=dh
LED_OFF=dl

LED_RED=16
LED_GREEN=20
LED_BLUE=21

echo "LED GREEN ON."
/usr/bin/pinctrl $LED_GREEN op $LED_ON
