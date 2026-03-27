#!/bin/bash

### ラズパイが起動してからのパケット送信量(Byte)

TX_PACKET=`/sbin/ifconfig eth0 | /bin/grep 'TX packets' | /usr/bin/head -1 | /bin/sed -E 's/[\t ]+/ /g' | /usr/bin/cut -d ' ' -f 6`

echo "Send $TX_PACKET bytes after boot."
