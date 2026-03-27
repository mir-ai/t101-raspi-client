#!/bin/bash

### MP3ファイルを再生する（番号を数える）

ON=dh
OFF=dl

PIN_AUX_OUT=25

echo "GPIO AUX ON"
/usr/bin/pinctrl $PIN_AUX_OUT op $ON

echo "PLAYING"
/usr/bin/mpg123 ../mp3/female_number_0.mp3 \
../mp3/female_number_1.mp3 \
../mp3/female_number_2.mp3 \
../mp3/female_number_3.mp3 \
../mp3/female_number_4.mp3 \
../mp3/female_number_5.mp3 \
../mp3/female_number_6.mp3 \
../mp3/female_number_7.mp3 \
../mp3/female_number_8.mp3 \
../mp3/female_number_9.mp3

echo "GPIO AUX OFF"
/usr/bin/pinctrl $PIN_AUX_OUT op $OFF
