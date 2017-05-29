from sensorkit.MotorControl_L298N import MotorControl_L298N
import time

<<<<<<< HEAD
RIGHT = 1
FORWARD = 0
LEFT = -1
=======
>>>>>>> 853bfb8c9094baee2b673d2613ffe77a82c1e367

class SteeringMotor(MotorControl_L298N):

    def __init__(self, input_pin0, input_pin1, enable_pin, duty_cycle = 0, pwm_frequency = 100, center_angle= 50, hydraulic = True, name = "Steering Motor"):
        super(SteeringMotor, self).__init__(input_pin0=input_pin0, input_pin1=input_pin1, enable_pin=enable_pin, duty_cycle = duty_cycle, pwm_frequency=pwm_frequency, name=name)
        self.hydraulic = hydraulic
        self.current_state = 0
        self.center_angle = 50
<<<<<<< HEAD
        self.blockage = 0
        self.current_dir = 0

    def right(self):
        if self.blockage == RIGHT:
            return
        self.current_dir = RIGHT
        self.forward(speed=40)
        if self.blockage == LEFT:
            self.blockage = 0

    def left(self):
        if self.blockage == LEFT:
            return
        self.current_dir = LEFT
        self.backward(speed=40)
        if self.blockage == RIGHT:
            self.blockage = 0

    def forward_dir(self):
        if self.blockage == FORWARD:
            return
        if self.blockage == RIGHT:
            self.backward(speed = 40)
        elif self.blockage == LEFT:
            self.forward(speed = 40)
        self.current_dir = FORWARD

    def current_direction(self):
        return self.current_dir

    def set_blockage(self, direction):
        self.blockage = direction
=======

    def right(self):
        self.forward(speed=50)

    def left(self):
        self.backward(speed=50)
>>>>>>> 853bfb8c9094baee2b673d2613ffe77a82c1e367

    def angle(self, value):
        value = 100 if value > 100 else 0 if value < 0 else value
        if self.__getAngleStatePoint(value) != self.current_state:

            diff = self.__getAngleStatePoint(value) - self.current_state
            while diff != 0:
                if diff > 0: # we need to turn right
<<<<<<< HEAD
                    self.forward(speed = 40)
=======
                    self.forward(speed = 80)
>>>>>>> 853bfb8c9094baee2b673d2613ffe77a82c1e367
                    time.sleep(.3)
                    self.stop()
                    diff -= 1
                elif diff < 0:
<<<<<<< HEAD
                    self.backward(speed = 40)
=======
                    self.backward(speed = 80)
>>>>>>> 853bfb8c9094baee2b673d2613ffe77a82c1e367
                    time.sleep(.3)
                    self.stop()
                    diff += 1
            self.current_state = self.__getAngleStatePoint(value)
            print("Current state:", self.current_state)
            """
            if value > (self.center_angle + 25): # this means we need to set angle of steers full right
                self.forward(speed = 100)
                time.sleep(1.7)
                self.current_state = 2
                self.stop()
            elif value > self.center_angle:
                self.forward(speed = 100)
                time.sleep(.85)
                self.current_state = 1
                self.stop()
            elif value < (self.center_angle - 25):
                self.backward(speed = 100)
                time.sleep(1.7)
                self.current_state = -2
                self.stop()
            elif value < self.center_angle:
                self.backward(speed = 100)
                time.sleep(.85)
                self.current_state = -1
                self.stop()
            """


    def __runHydraulic(self):
        print("Hydraulic: current_state",self.current_state)
        self.angle(self.center_angle)
        self.current_state = 0

    def __getAngleStatePoint(self, value):
        if value > (self.center_angle + 15):
            return 1
        elif value < (self.center_angle - 10):
            return -1
        else:
            return 0
