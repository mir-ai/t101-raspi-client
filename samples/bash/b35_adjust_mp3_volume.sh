#!/bin/bash

MAX_VOLUME=`ffmpeg -i /tmp/record.mp3 -af volumedetect -f null - 2>&1 | grep 'max_volume:' | cut -d ':' -f 2 | cut -d ' ' -f 2`

echo "max volume of /tmp/record.mp3 is $MAX_VOLUME dB"

# マイナスを除去
ADD_VOLUME=${MAX_VOLUME#-}dB

ffmpeg -y -i /tmp/record.mp3 -af volume=$ADD_VOLUME -c:v copy /tmp/record_adjusted.mp3


### 再生する。

ON=dh
OFF=dl

PIN_AUX_OUT=25

# スピーカーON
echo "GPIO AUX ON"
/usr/bin/pinctrl $PIN_AUX_OUT op $ON

# 再生
echo "PLAYING"
/usr/bin/mpg123 /tmp/record_adjusted.mp3

# スピーカーOFF
echo "GPIO AUX OFF"
/usr/bin/pinctrl $PIN_AUX_OUT op $OFF
