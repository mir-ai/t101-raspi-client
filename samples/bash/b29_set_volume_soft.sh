#!/bin/bash

### 音量を大きく設定する (50)

VOLUME=`/usr/bin/amixer sset Master 50% | grep 'Front Left: Playback' | cut -d '[' -f 2 | cut -d '%' -f 1`

echo "Set volume to $VOLUME"
