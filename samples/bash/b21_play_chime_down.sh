#!/bin/bash

### MP3ファイルを再生する（下りチャイム）

ON=dh
OFF=dl

PIN_AUX_OUT=25

# スピーカーON
echo "GPIO AUX ON"
/usr/bin/pinctrl $PIN_AUX_OUT op $ON

# 再生
echo "PLAYING"
/usr/bin/mpg123 ../mp3/chime_down.mp3

# スピーカーOFF
echo "GPIO AUX OFF"
/usr/bin/pinctrl $PIN_AUX_OUT op $OFF
