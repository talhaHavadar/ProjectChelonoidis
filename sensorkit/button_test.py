import RPi.GPIO as io
from sensorkit.Button import Button
import time

button = Button(input_pin=4, name="Left wheel detector")

def button_pressed():
    print("Button Pressed!!")

button.setup()
button.set_callback(button_pressed)

try:
    while True:
        print("Looping..")
        time.sleep(0.5)
except:
    io.cleanup()
