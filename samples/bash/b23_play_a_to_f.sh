#!/bin/bash

### MP3ファイルを再生する（番号を数える）

ON=dh
OFF=dl

PIN_AUX_OUT=25

# スピーカーON
echo "GPIO AUX ON"
/usr/bin/pinctrl $PIN_AUX_OUT op $ON

# 再生
echo "PLAYING"
/usr/bin/mpg123 ../mp3/female_alpha_a.mp3 \
../mp3/female_alpha_b.mp3 \
../mp3/female_alpha_c.mp3 \
../mp3/female_alpha_d.mp3 \
../mp3/female_alpha_e.mp3 \
../mp3/female_alpha_f.mp3

# スピーカーOFF
echo "GPIO AUX OFF"
/usr/bin/pinctrl $PIN_AUX_OUT op $OFF
