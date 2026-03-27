#!/bin/bash

### 空きメモリの%を取得する

MEM_AVAILABLE=`/usr/bin/free | /bin/grep -oP "Mem:.*" | /usr/bin/awk '{print $7}'`
MEM_TOTAL=`/usr/bin/free | /bin/grep -oP "Mem:.*" | /usr/bin/awk '{print $2}'`
MEM_FREE_PERCENT=$(( $(( $MEM_AVAILABLE * 100 )) / $MEM_TOTAL ))

echo "Memory available = $MEM_AVAILABLE KB, Total memory = $MEM_TOTAL KB, ($MEM_FREE_PERCENT% FREE)"