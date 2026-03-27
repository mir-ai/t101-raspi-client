#!/bin/bash

### 起動してからの秒数を取得する

BOOT_DATETIME=`/usr/bin/uptime -s`
BOOT_UNIXTIME=`/bin/date -d "${BOOT_DATETIME}" +%s`
CUR_UNIXTIME=`/bin/date +%s`
MIN_SINCE_BOOT=$((CUR_UNIXTIME-BOOT_UNIXTIME))

echo "$MIN_SINCE_BOOT seconds since boot."
