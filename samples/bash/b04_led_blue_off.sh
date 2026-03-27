#!/bin/bash

### 青のLEDを消灯する

LED_ON=dh
LED_OFF=dl

LED_RED=16
LED_GREEN=20
LED_BLUE=21

echo "LED BLUE OFF."
/usr/bin/pinctrl $LED_BLUE op $LED_OFF
