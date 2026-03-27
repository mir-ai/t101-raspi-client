#!/bin/bash

# wavファイルを mp3 に変換する
echo "/tmp/record.wav to /tmp/record.mp3"

ffmpeg -y -i /tmp/record.wav -vn -ac 1 -ar 22050 -ab 96k -acodec libmp3lame -f mp3 /tmp/record.mp3



