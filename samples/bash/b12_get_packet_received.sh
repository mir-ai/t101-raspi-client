#!/bin/bash

### ラズパイが起動してからのイーサーネットでのパケット受信量(バイト) 

RX_PACKET=`/sbin/ifconfig eth0 | /bin/grep 'RX packets' | /usr/bin/head -1 | /bin/sed -E 's/[\t ]+/ /g' | /usr/bin/cut -d ' ' -f 6`

echo "Reviceved $RX_PACKET bytes after boot."
