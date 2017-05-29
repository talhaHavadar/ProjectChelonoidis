from sensorkit.Button import Button
from sensorkit.MotorControl_L298N import MotorControl_L298N
import steering

#CMD#AP|FORWARD;FORWARD@1491654579794#END#

forwardw_button = Button(input_pin=15, name="Forward Wheel Detector")
rightw_button = Button(input_pin=4, name="Right Wheel Detector")
leftw_button = Button(input_pin=14, name="Left Wheel Detector")
steering_motor = steering.SteeringMotor(input_pin0=17, input_pin1=27, enable_pin=22)
motor = MotorControl_L298N(input_pin0=10, input_pin1=9, enable_pin=11)

forwardw_button.setup()
leftw_button.setup()
rightw_button.setup()

def rightw_button_pressed():
    print("RIGHT")
    if steering_motor.current_direction() == steering.RIGHT:
        steering_motor.stop()
        steering_motor.set_blockage(steering.RIGHT)

def leftw_button_pressed():
    print("LEFT")
    if steering_motor.current_direction() == steering.LEFT:
        steering_motor.stop()
        steering_motor.set_blockage(steering.LEFT)

def forwardw_button_pressed():
    print("FORWARD")
    if steering_motor.current_direction() == steering.FORWARD:
        steering_motor.stop()
        steering_motor.set_blockage(steering.FORWARD)

forwardw_button.set_callback(forwardw_button_pressed)
leftw_button.set_callback(leftw_button_pressed)
rightw_button.set_callback(rightw_button_pressed)

try:

    while True:
        cmd = input("Command:")
        if cmd == "right":
            steering_motor.right()
        elif cmd == "left":
            steering_motor.left()
        elif cmd == "f":
            steering_motor.forward_dir()
        elif cmd == "s":
            steering_motor.stop()
        elif cmd == "q":
            break
except Exception:
    pass

leftw_button.cleanup()
rightw_button.cleanup()
forwardw_button.cleanup()
steering_motor.cleanup()
motor.cleanup()

print("DONE.")
