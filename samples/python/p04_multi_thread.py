#!/usr/bin/python3
# coding: utf-8

import os
import sys
import time
import traceback
import threading

def thread_1():
    for i in range(10, 19):
        print (f"thread_1 {i}")
        time.sleep(1)

def thread_2():
    for i in range(20, 29):
        print (f"\t\t thread_2 {i}")
        time.sleep(1)

def thread_3():
    for i in range(30, 39):
        print (f"\t\t\t\t thread_3 {i}")
        time.sleep(1)

th1 = threading.Thread(
    target=thread_1,
    daemon=True,
)

th2 = threading.Thread(
    target=thread_2,
    daemon=True,
)

th3 = threading.Thread(
    target=thread_3,
    daemon=True,
)

# スレッドを開始する
th1.start()
th2.start()
th3.start()

# スレッドの終了を待つ
th1.join()
th2.join()
th3.join()

