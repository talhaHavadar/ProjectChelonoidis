#-*- coding: utf-8 -*-
# echo pin on GPIO 17
# trig pin on GPIO 27

from RPi import GPIO as io
from sensorkit.UltrasonicHCSR04 import UltrasonicHCSR04
import time
import threading

usensor = UltrasonicHCSR04(trig_pin = 17, echo_pin = 27, name = "Efsanevi Sensör")
get_measurement = True
def ultrasonicsensors():
    print threading.currentThread().getName(), " starting.."
    while get_measurement:
        try:
            print(usensor.getDistance())
            time.sleep(.5)
        except KeyboardInterrupt:
            io.cleanup()
t = threading.Thread(name= "Usensor Thread", target = ultrasonicsensors)
t.start()
time.sleep(20)
get_measurement = False
usensor.cleanup()
