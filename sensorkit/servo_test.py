import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 50)
pwm.start(5)
GPIO.setwarnings(False)

duty = float(80) / 18.0 + 2.5
pwm.ChangeDutyCycle(duty)

while True:
    command = raw_input("Enter an angle or write 'exit' to stop: ")
    if command == "exit":
        break
    duty = float(command) / 18.0 + 2.5
    pwm.ChangeDutyCycle(duty)

GPIO.cleanup()
