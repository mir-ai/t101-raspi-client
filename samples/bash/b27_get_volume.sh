#!/bin/bash

### 音量を取得する

VOLUME=`/usr/bin/amixer sget Master | grep 'Front Left: Playback' | cut -d '[' -f 2 | cut -d '%' -f 1`

echo "Current volume = $VOLUME"


