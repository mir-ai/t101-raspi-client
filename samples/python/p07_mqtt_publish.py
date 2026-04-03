#!/usr/bin/python3
# coding: utf-8

import time
import threading
import json
from _thread import interrupt_main
import urllib.request
import traceback
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import ssl
import sys
from MirMqtt import Mqtt
from MirPlatformRaspi import PlatformRaspi

device_cpu_id = PlatformRaspi._get_device_cpu_id_raspi()

TOPIC_UPSTREAM = 'mqtt/training/t102/upstream/999999'

Mqtt.init(
    topic=TOPIC_UPSTREAM,
    client_id=f"t102_training_{device_cpu_id}"
)

try:
    Mqtt.mqttc = Mqtt.connect_mqtt()
    print(4101, f"OK MQTT thread start, subscribe topic '{Mqtt.TOPIC}'", 'ST_MQTT_START')

    msg_count = 0
    for i in range(3):

        payload = {
            'log_type': 'MQTT_LOG',
            'log_body': f"{device_cpu_id} p07_mqtt_publish {i}",
            'unixtime': time.time()
        }
        payload_json_string = json.dumps(payload)

        qos = 0
        result = Mqtt.mqttc.publish(Mqtt.TOPIC, payload_json_string, qos)

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send topic `{Mqtt.TOPIC}` message={payload_json_string}")
        else:
            print(f"Failed to send message to topic {Mqtt.TOPIC}")

        time.sleep(1)

except Exception as e:
    print(4109, f"NG MQTT thread failed: {e}", 'ERR_MQTT_FAILED')

    # interrupt the main thread
    interrupt_main()

