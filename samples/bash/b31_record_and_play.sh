#!/bin/bash

### REC_SECONDS秒間録音する。

REC_SECONDS=5

RECORD_DEVICE=`/usr/bin/arecord -L | grep plughw:`

echo "Recording. Please speak something."
/usr/bin/arecord --device $RECORD_DEVICE --channels 1 --format S16_LE --rate 22050 -d $REC_SECONDS /tmp/record.wav

### 再生する。

ON=dh
OFF=dl

PIN_AUX_OUT=25

# スピーカーON
echo "GPIO AUX ON"
/usr/bin/pinctrl $PIN_AUX_OUT op $ON

# 音源再生
echo "PLAYING"
aplay /tmp/record.wav

# スピーカーOFF
echo "GPIO AUX OFF"
/usr/bin/pinctrl $PIN_AUX_OUT op $OFF
