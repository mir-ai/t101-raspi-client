#!/bin/bash

### IPアドレスを取得する

# eth0のMACアドレスを取得する
MY_IP_ADDRESS=`ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'`

echo "My ip address is $MY_IP_ADDRESS"
