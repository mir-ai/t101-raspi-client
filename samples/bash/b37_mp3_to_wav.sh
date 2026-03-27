#!/bin/bash

# wavファイルを mp3 に変換する
echo "/tmp/record.mp3 to /tmp/record_mp3.wav"

ffmpeg -y -i /tmp/record.mp3 -vn -ac 1 -ar 44100 -acodec pcm_s16le -f wav /tmp/record_mp3.wav
