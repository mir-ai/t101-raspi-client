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

TOPIC = 'mqtt/training/t102/downstream/999999'

Mqtt.init(
    topic=TOPIC,
    client_id=f"t102_training_{device_cpu_id}"
)

while True:
    try:
        Mqtt.mqttc = Mqtt.connect_mqtt()


        # Subscribe TOPIC
        Mqtt.mqttc.subscribe(Mqtt.TOPIC, qos = 0)

        print(4101, f"OK MQTT thread start, subscribe topic '{Mqtt.TOPIC}'", 'ST_MQTT_START')

        # Loop forever
        Mqtt.mqttc.loop_forever()

    except Exception as e:
        print(4109, f"NG MQTT thread failed: {e}", 'ERR_MQTT_FAILED')

        # interrupt the main thread
        interrupt_main()

    time.sleep(1)
