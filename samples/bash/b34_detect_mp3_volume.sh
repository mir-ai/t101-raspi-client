#!/bin/bash

MAX_VOLUME=`ffmpeg -i /tmp/record.mp3 -af volumedetect -f null - 2>&1 | grep 'mean_volume:' | cut -d ':' -f 2 | cut -d ' ' -f 2`

echo "max volume of /tmp/record.mp3 is $MAX_VOLUME dB"


