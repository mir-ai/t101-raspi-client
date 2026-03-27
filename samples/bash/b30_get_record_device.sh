#!/bin/bash

### 録音用のデバイス名を取得する

RECORD_DEVICE=`/usr/bin/arecord -L | grep plughw:`

echo "Record device=$RECORD_DEVICE"
