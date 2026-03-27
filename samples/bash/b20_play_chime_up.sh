#!/bin/bash

### MP3ファイルを再生する（上りチャイム）

ON=dh
OFF=dl

PIN_AUX_OUT=25

echo "GPIO AUX ON"
/usr/bin/pinctrl $PIN_AUX_OUT op $ON

echo "PLAYING"
/usr/bin/mpg123 ../mp3/chime_up.mp3

echo "GPIO AUX OFF"
/usr/bin/pinctrl $PIN_AUX_OUT op $OFF
