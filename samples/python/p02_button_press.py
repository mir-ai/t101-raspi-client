#!/usr/bin/python3
# coding: utf-8

from gpiozero import Button
import time

def ac_down_pressed():
    print ('AC_DOWN')

def ac_down_released():
    print ('AC_DOWN restored')

def low_battery_pressed():
    print ('LOW_BATTERY')

def low_battery_released():
    print ('LOW_BATTERY restored')

def door_open_pressed():
    print ('DOOR_OPEN')

def door_open_released():
    print ('DOOR_OPEN restored')


PIN_AC_DOWN="GPIO10"
PIN_LOW_BATTERY="GPIO9"
PIN_DOOR_OPEN="GPIO11"

button_ac_down = Button(PIN_AC_DOWN)
button_ac_down.when_pressed = ac_down_pressed
button_ac_down.when_released = ac_down_released

button_low_battery = Button(PIN_LOW_BATTERY)
button_low_battery.when_pressed = low_battery_pressed
button_low_battery.when_released = low_battery_released

button_door_open = Button(PIN_DOOR_OPEN)
button_door_open.when_pressed = door_open_pressed
button_door_open.when_released = door_open_released

print ("Press button AC_DOWN, LOW_BATTER, DOOR_OPEN. Press Ctrl-C to exit.")
while (True):
    time.sleep(1)

