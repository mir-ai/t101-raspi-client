#!/bin/bash

### REC_SECONDS秒間録音する。

REC_SECONDS=5

RECORD_DEVICE=`/usr/bin/arecord -L | grep plughw:`

echo "Recording. Please speak something."
/usr/bin/arecord --device $RECORD_DEVICE --channels 1 --format S16_LE --rate 22050 -d $REC_SECONDS /tmp/record.wav

# wavファイルを mp3 に変換する
ffmpeg -y -i /tmp/record.wav -vn -ac 1 -ar 22050 -ab 96k -acodec libmp3lame -f mp3 /tmp/record.mp3

# AWS の S3 にアップロードする
echo
echo "Uploading to S3..."

aws s3 cp /tmp/record.mp3 s3://ss-a-alert/uploaded_mp3/2601/record.mp3 --acl public-read --profile=mms-catcher-mp3-uploader

echo "Uploaded. "
echo
echo "Check https://ss-a-alert.s3.ap-northeast-1.amazonaws.com/uploaded_mp3/2601/record.mp3"
