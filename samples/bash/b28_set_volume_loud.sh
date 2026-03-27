#!/bin/bash

### 音量を大きく設定する (70)

VOLUME=`/usr/bin/amixer sset Master 70% | grep 'Front Left: Playback' | cut -d '[' -f 2 | cut -d '%' -f 1`

echo "Set volume to $VOLUME"
