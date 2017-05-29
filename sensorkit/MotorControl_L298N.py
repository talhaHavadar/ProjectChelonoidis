from RPi import GPIO as io
import time

class MotorControl_L298N(object):

    def __init__(self, input_pin0, input_pin1, enable_pin, duty_cycle = 0, pwm_frequency = 100 , name = "MotorControl Circuit"):
        self.input_pin0 = input_pin0
        self.input_pin1 = input_pin1
        self.enable_pin = enable_pin
        self.is_ready = False
        self.name = name
        self.duty_cycle = duty_cycle
        self.pwm_frequency = pwm_frequency
        self.__setup();

    def __setup(self):
        print("[-] %s is setting up.." %(self.name))
        io.setmode(io.BCM)
        io.setup(self.input_pin0, io.OUT, initial = io.LOW)
        io.setup(self.input_pin1, io.OUT, initial = io.LOW)
        io.setup(self.enable_pin, io.OUT)
        self.pwm = io.PWM(self.enable_pin, self.pwm_frequency)
        self.pwm.start(self.duty_cycle)
        time.sleep(2)
        self.is_ready = True
        print("[-] Setup completed")

    def __setDutyCycle(self, duty_cycle):
        self.duty_cycle = duty_cycle
        self.pwm.ChangeDutyCycle(self.duty_cycle)

    def setSpeed(self, speed):
        if not self.is_ready:
            self.__setup()

        if(speed <= 100 and speed >= 0):
            self.__setDutyCycle(speed)
        elif(speed > 100):
            print("speed value undefined")
            return -1

    def forward(self, speed = None):
        if not self.is_ready:
            self.__setup()
        if speed is not None:
            self.setSpeed(speed)

        io.output(self.input_pin0, True)
        io.output(self.input_pin1, False)

    def backward(self, speed = None):
        if not self.is_ready:
            self.__setup()
        if speed is not None:
            self.setSpeed(speed)

        io.output(self.input_pin0, False)
        io.output(self.input_pin1, True)

    def stop(self):
        io.output(self.input_pin0, False)
        io.output(self.input_pin1, False)

    def cleanup(self):
        io.cleanup((self.input_pin0, self.input_pin1, self.enable_pin))
        self.pwm.stop()
        self.is_ready = False
