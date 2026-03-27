#!/bin/bash

### MACアドレスを取得する

# eth0のMACアドレスを取得する
MY_MAC_ADDRESS=`/sbin/ifconfig eth0 | /bin/grep 'ether' | /usr/bin/awk '{gsub(/:/, ""); print $2}'`

if [ "$MY_MAC_ADDRESS" = "" ] ; then
  # eth0に接続されていない場合はそれ以外のMACアドレスを取得する
  MY_MAC_ADDRESS=`/sbin/ifconfig | /usr/bin/sort | /bin/grep 'ether' | /usr/bin/awk '{gsub(/:/, ""); print $2}'`
fi

echo "My mac address is $MY_MAC_ADDRESS"
