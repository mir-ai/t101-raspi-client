#!/bin/bash

### 8.8.8.8 に ping で通信したときの応答ミリセカンド

PING_MS=`ping -c 1 -s 1024 8.8.8.8 | tail -1 | cut -d '/' -f  6`

echo "The ping response time to 8.8.8.8 (1024 byte) was $PING_MS ms."
