from steering import SteeringMotor
from sensorkit.MotorControl_L298N import MotorControl_L298N
import socketserver
import time
import socket
import commands
import handlers
import threading

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind(("", 4444))





#steering_motor = SteeringMotor(input_pin0=17, input_pin1=27, enable_pin=22)

#motor = MotorControl_L298N(input_pin0=10, input_pin1=9, enable_pin=11, pwm_frequency = 20)

#cmd_handler = commands.CommandsHandler(pool_size = 10)

server = handlers.AsyncTCPServer(("0.0.0.0", 4444), handlers.TCPSocketHandler)
server_info = server.server_address

server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()
print("Server info:", server_info)
print("Server thread started with name: ", server_thread.name)

inp = input()
server.shutdown()
server.server_close()
"""
# motor.forward(100)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

try:
    # We are expecting an input between 0 and 100 to control steering angle
    # Because of the hardware insufficiency problem, We have to use DC Motor
    # and to provide angular motion, we used time domain.

    while True:
        data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
        print("received message:", data, "address:", addr)
        cmd = commands.Command(command_string=str(data))
        cmd_handler.addCommand(cmd)
        mvmnt_cmd = cmd_handler.lastCommand(commands.COMMAND_TYPE_MOVEMENT_CONTROL)
        yaxis = int(mvmnt_cmd.arguments[1])
        xaxis = int(mvmnt_cmd.arguments[0])
        angle = 50
        if xaxis > 38:
            angle = translate(xaxis, 39, 99, 51, 100)
            print("right", angle)
            if angle < 65:
                steering_motor.stop()
            else:
                steering_motor.right()
            # steering_motor.angle(angle)
        elif xaxis < 38:
            angle = translate(xaxis, 0, 37, 0, 49)
            print("left", angle)
            if angle > 35:
                steering_motor.stop()
            else:
                steering_motor.left()
            # steering_motor.angle(angle)
        else:
            steering_motor.angle(50)
        speed = 0
        if yaxis > 39:
            speed = translate(yaxis, 40, 100, 0, 80)
            print("backward", speed)
            motor.backward(speed)
        elif yaxis < 39:
            speed = translate(yaxis, 38, 0, 0, 80)
            print("forward", speed)
            motor.forward(speed)
        else:
            motor.stop()
        print("Last Movement Command:", cmd_handler.lastCommand(commands.COMMAND_TYPE_MOVEMENT_CONTROL))
        print("Last Sensor Command:", cmd_handler.lastCommand(commands.COMMAND_TYPE_ULTRASONIC_SENSOR))
        # angle = int(input("Enter steering angle between 100 and 0:"))
        # print("Angle:", angle)
        # steering_motor.angle(angle)

except Exception:
    steering_motor.cleanup()
    motor.cleanup()
"""
