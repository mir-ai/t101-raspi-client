#!/bin/bash

ON=dh
OFF=dl

PIN_AUX_OUT=25

# AWS の S3 からダウンロードする

wget https://ss-a-alert.s3.ap-northeast-1.amazonaws.com/uploaded_mp3/2601/record.mp3 -O /tmp/downloaded.mp3

# スピーカーON
echo "GPIO AUX ON"
/usr/bin/pinctrl $PIN_AUX_OUT op $ON

# 再生
echo "PLAYING"
/usr/bin/mpg123 ../mp3/chime_up.mp3 /tmp/downloaded.mp3 ../mp3/chime_down.mp3

# スピーカーOFF
echo "GPIO AUX OFF"
/usr/bin/pinctrl $PIN_AUX_OUT op $OFF
