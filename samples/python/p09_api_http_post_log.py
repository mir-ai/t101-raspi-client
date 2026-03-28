#!/usr/bin/python3
# coding: utf-8

import urllib.request
import json
import traceback
import time

url = 'https://rd.mir-ai.net/api/log/post'
payload = {
    'log_type' : 'P09',
    'log_body' : 'TEST テスト',
    'unixtime' : time.time()
}
timeout = 3

headers = {
    'Content-Type': 'application/json',
    'X-miraie-client': 'ccbox01'
}

req = urllib.request.Request(
    url=url, 
    data=json.dumps(payload).encode('utf-8'), 
    headers=headers
)

try:
    print(f"HTTP request Http POST: {url}")

    with urllib.request.urlopen(req, timeout=timeout) as fp:
        content = fp.read().decode('utf-8')
        content = content.strip()
        try:
            data = json.loads(content)
            http_status = fp.status
            print (f"{http_status}", data)

        except Exception as e:
            print(f"Corrupted JSON from http_post api. URL='{url}'." + str(e))

except Exception as e:
    print(f"failed to post URL={url} : " + str(e))
