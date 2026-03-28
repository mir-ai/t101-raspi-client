#!/usr/bin/python3
# coding: utf-8

from gpiozero import LEDBoard
import time

PIN_LED_RED="GPIO16"
PIN_LED_GREEN="GPIO20"
PIN_LED_BLUE="GPIO21"

led_device = LEDBoard(
    PIN_LED_RED,
    PIN_LED_GREEN,
    PIN_LED_BLUE,
    pwm=False
)

#                   赤 緑 青
# 青
led_device.value = (0, 0, 1)
time.sleep(1)

# シアン
led_device.value = (0, 1, 1)
time.sleep(1)

# 白
led_device.value = (1, 1, 1)
time.sleep(1)

# 黄色
led_device.value = (1, 1, 0)
time.sleep(1)

# 緑
led_device.value = (0, 1, 0)
time.sleep(1)

# 赤
led_device.value = (1, 0, 0)
time.sleep(1)

# 紫
led_device.value = (1, 0, 1)
time.sleep(1)

# 消灯
led_device.value = (0, 0, 0)
time.sleep(1)
