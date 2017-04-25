"""
Servo Module to provide easy controlling for servo motors.


@author: Talha Havadar
"""
import RPi.GPIO as io

class BaseServo(object):
    """Base class for servo motor controlling.

    Attributes:
        frequency: int --default: 50 # select correct frequency for not hurt the motor
                    and to prevent overheating(if your motor expects pulse every 20ms then give 50hz frequency)
        data_pin: int # the pin that we control the servo
    """
    def __init__(self, data_pin, frequency=50):
        super(BaseServo, self).__init__()
        self.frequency = frequency
        self.data_pin = data_pin

class TowerProMG995(BaseServo):
    """Specific servo configuration for TowerPro MG995

    Attributes:
        name: str --default: TowerPro MG995
        angle_controller : GPIO.PWM # pwm controller for servo this will be generated after setup method.
    Properties:
        angle: int
    Method:
        is_ready() -> bool # returns servo motor status if it is ready then you can change the angle if it is not you need call setup method
        setup() # sets up the servo
        cleanup() # cleans up the pins that used by servo
    """


    def __init__(self, data_pin, name="TowerPro MG995"):
        super(TowerProMG995, self).__init__(data_pin=data_pin, frequency=50)
        self.name = name

    def setup(self, initial_angle = 0):
        """Initializes the servo."""
        print("%s setting up.." % (self.name))
        io.setup(self.data_pin, io.OUT)
        self.angle_controller = io.PWM(self.data_pin, self.frequency)
        self.angle_controller.start(self.__calculate_duty(initial_angle))
        self._current_angle = initial_angle
        self._is_ready = True
        print("%s setup is completed." % (self.name))

    @property
    def angle(self):
        return self._current_angle

    @angle.setter
    def angle(self, value):
        if not self.is_ready():
            raise RuntimeError("Servo is not ready! Please be sure about you called the setup method of class before.")
        if value > 180 or value < 0:
            raise ValueError("Angle value must be between 0 and 180")
        if not isinstance(value, int):
            raise TypeError("Angle must be integer.")
        if self.angle_controller is None:
            raise ValueError("angle_controller is None. Please be sure you called setup method.")
        self.angle_controller.ChangeDutyCycle(self.__calculate_duty(value))
        self._current_angle = value


    def cleanup(self):
        """Cleans up the pins taht used by servo.After called this method, if you want to start using the same servo you need to call setup method again."""
        if not self.is_ready():
            raise RuntimeWarning("You are trying to cleanup the servo that has not been setted up yet.")
        self._is_ready = False
        self.angle_controller.stop()
        io.cleanup((self.data_pin))
        self._current_angle = 0
        self.angle_controller = None

    def is_ready(self):
        return self._is_ready;


    def __calculate_duty(self, angle):
        """Returns correct value for the given angle. Angle must be between 0 and 180"""
        return float(angle) / 18.0 + 2.5
