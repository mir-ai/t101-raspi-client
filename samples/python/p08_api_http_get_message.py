#!/usr/bin/python3
# coding: utf-8

import urllib.request
import json
import traceback
import time

url = 'https://rd.mir-ai.net/api/message/latest'
timeout = 3

try:
    req = urllib.request.Request(url)
    req.add_header('X-miraie-client', 'ccb1')

    print(f"HTTP request Http GET: {url}")

    with urllib.request.urlopen(req, timeout=timeout) as fp:
        content = fp.read().decode('utf-8')
        content = content.strip()
        try:
            data = json.loads(content)
            http_status = fp.status

            print (f"{http_status}", data)
        except Exception as e:
            print(f"JSON corrupted {url}, '{content}'." + str(e))
            pass
except Exception as e:
    print (f"NG Unable to access {url} :" + str(e))
