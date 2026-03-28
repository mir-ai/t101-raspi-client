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

# log_code 4100

# 下位ライブラリ
# クラウドから更新指示をMQTTで受信する
# 
# 用途：
# プレイリストの更新や遠隔コマンド発行があったときに、MQTTで通知されるので、それをきっかけにして
# 更新タイムスタンプをチェックの上、プレイリストのJSONや遠隔コマンドの取得APIにアクセスする。
#
# MQTTが落ちたときのために、別途90秒ごとにも更新タイムスタンプファイルをチェックして、更新があったらプレイリストのJSONや遠隔コマンドの取得APIにアクセスする処理も並行して走っています。
class Mqtt:
    
    TOPIC = ''
    CLIENT_ID = ''

    # AWS Iot Coreへの接続情報
    HOST = 'af4m59y099o4d-ats.iot.ap-northeast-1.amazonaws.com'
    PORT = 8883
    KEEP_ALIVE=60

    # AWS Iot Coreに接続するための認証キー
    CA_CERTS = '../../awsiot_certs/250129/AmazonRootCA1.pem'
    CERTFILE = '../../awsiot_certs/250129/c3c5a040a8958d1c7ddc398e5c34b33929e86a4bab50b07a0b88c69a287768e2-certificate.pem.crt'
    #CLIENT_PUBLIC = 'awsiot_certs/250129/c3c5a040a8958d1c7ddc398e5c34b33929e86a4bab50b07a0b88c69a287768e2-public.pem.key'
    KEYFILE = '../../awsiot_certs/250129/c3c5a040a8958d1c7ddc398e5c34b33929e86a4bab50b07a0b88c69a287768e2-private.pem.key'

    # MQTT Client
    mqttc = None

    # Connected
    just_connected = False

    # MQTTを初期化
    def init(
            topic: str,
            client_id: str,
    ):
        Mqtt.TOPIC = topic
        Mqtt.CLIENT_ID = client_id
    
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        if flags["session present"] == 1:
            # ...
            print(f"MQTT onconnect Session present")

        if rc == 0:
            # 接続したらサブスクライブ開始
            #client.subscribe(Mqtt.TOPIC, qos = 1)

            # success connect
            print(f"MQTT Connected with result code {rc}, subscribe topic={Mqtt.TOPIC}")

        if rc > 0:
            # error processing
            print(f"MQTT Failed to connect: {rc}. loop_forever() will retry connection")

    # 切断時
    def on_disconnect(client, userdata, rc):
        if rc == 0:
            print(f"Disconnected with result code {rc}")
            # success disconnect
        if rc > 0:
            # error processing
            print(f"Disconnected failed with result code {rc}")

    # 購読時
    def on_subscribe(client, userdata, mid, granted_qos):
        for sub_result in granted_qos:
            # Since we subscribed only for a single channel, reason_code_list contains
            # a single entry
            if sub_result == 1:
                # process QoS == 1
                print(f"Broker granted the following QoS: 1")

            if sub_result == 0x80:
                # error processing
                print(f"Broker rejected you subscription")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

        data = {}
        try:
            data = json.loads(msg.payload)
            print ("MQTT message received", data)
        except Exception as e:
            print(f"MQTT message json corrupted '{msg.payload}'" + str(e))

    def connect_mqtt():
        mqttc = mqtt.Client(protocol=mqtt.MQTTv311)
        mqttc.enable_logger()
        mqttc.on_connect = Mqtt.on_connect
        mqttc.on_message = Mqtt.on_message
        mqttc.on_disconnect = Mqtt.on_disconnect
        mqttc.tls_set(
            ca_certs = Mqtt.CA_CERTS,
            certfile = Mqtt.CERTFILE,
            keyfile = Mqtt.KEYFILE,
            tls_version = ssl.PROTOCOL_TLSv1_2,
        )

        # AWS Iot Core MQTT サーバに接続する
        mqttc.connect(
            host=Mqtt.HOST,
            port=Mqtt.PORT, 
            keepalive=Mqtt.KEEP_ALIVE,
        )

        return mqttc

    def is_connected():
        if not Mqtt.mqttc:
            return False
        
        is_connected = False
        try:
            is_connected = Mqtt.mqttc.is_connected()
        except Exception as e:
            pass
        
        return is_connected
