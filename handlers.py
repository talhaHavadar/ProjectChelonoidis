import socketserver
import steering
from sensorkit.Button import Button
from sensorkit.MotorControl_L298N import MotorControl_L298N
from sensorkit.UltrasonicHCSR04 import UltrasonicHCSR04
import commands
import threading
import time

def AnotherThread(fn):
    """
        Decorator implementation of threading.
    """
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=fn, args=args, kwargs=kwargs)
        t.start()
        return t
    return wrapper

class AsyncTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class TCPSocketHandler(socketserver.StreamRequestHandler):

    cmd_handler = None

    def initiate(self):
        self.cmd_handler = commands.CommandsHandler(pool_size = 25)
        self.steering_motor = steering.SteeringMotor(input_pin0=17, input_pin1=27, enable_pin=22)
        self.motor = MotorControl_L298N(input_pin0=10, input_pin1=9, enable_pin=11)

        self.rightw_button = Button(input_pin = 4, name = "Right Wheel Detector")
        self.leftw_button = Button(input_pin = 14, name = "Left Wheel Detector")
        self.forwardw_button = Button(input_pin=15, name="Forward Wheel Detector")
        self.rightw_button.setup()
        self.leftw_button.setup()
        self.forwardw_button.setup()
        self.forwardw_button.set_callback(self.forward_button_pressed)
        self.rightw_button.set_callback(self.right_button_pressed)
        self.leftw_button.set_callback(self.left_button_pressed)

        # 18, 23
        self.left_usensor = UltrasonicHCSR04(trig_pin= 18, echo_pin= 23, name = "Left Ultrasonic Sensor")
        self.right_usensor = UltrasonicHCSR04(trig_pin= 24, echo_pin= 25, name = "Right Ultrasonic Sensor")
        self.front_usensor = UltrasonicHCSR04(trig_pin= 5, echo_pin= 6, name = "Front Ultrasonic Sensor")
        self.back_usensor = UltrasonicHCSR04(trig_pin= 20, echo_pin= 21, name = "Back Ultrasonic Sensor")
        self.get_measurement = True
        self.distance_interrupt = False
        self.handleUltrasonicSensors()

    def cleanup(self):
        self.steering_motor.cleanup()
        self.motor.cleanup()

        self.rightw_button.cleanup()
        self.leftw_button.cleanup()
        self.forwardw_button.cleanup()

        self.right_usensor.cleanup()
        self.left_usensor.cleanup()
        self.front_usensor.cleanup()
        self.back_usensor.cleanup()

    def forward_button_pressed(self):
        print("button_pressed(forward direction wheel)", self.steering_motor.current_direction())
        if self.steering_motor.current_direction() == steering.FORWARD:
            self.steering_motor.stop()
            self.steering_motor.set_blockage(steering.FORWARD)

    def left_button_pressed(self):
        print("button_pressed(left wheel)", self.steering_motor.current_direction())
        if self.steering_motor.current_direction() == steering.LEFT:
            self.steering_motor.stop()
            self.steering_motor.set_blockage(steering.LEFT)

    def right_button_pressed(self):
        print("button_pressed(right wheel): ", self.steering_motor.current_direction())
        # right wheel detector
        if self.steering_motor.current_direction() == steering.RIGHT:
            self.steering_motor.stop()
            self.steering_motor.set_blockage(steering.RIGHT)

    @AnotherThread
    def handleUltrasonicSensors(self):
        print(threading.currentThread().getName(), "starting..")
        while self.get_measurement:
            f_dist = self.front_usensor.getDistance() # index-0
            r_dist = self.right_usensor.getDistance() # index-1
            l_dist = self.left_usensor.getDistance() # index-2
            b_dist = self.back_usensor.getDistance() # index-3
            if f_dist <= 20:
                self.motor.stop()
                self.distance_interrupt = True
            else:
                self.distance_interrupt = False
            timestamp = int(time.time() * 1000.0)
            self.wfile.write("#CMD#US|0;{}@{}#END#\n".format(f_dist, str(timestamp)).encode())
            self.wfile.write("#CMD#US|1;{}@{}#END#\n".format(r_dist, str(timestamp)).encode())
            self.wfile.write("#CMD#US|2;{}@{}#END#\n".format(l_dist, str(timestamp)).encode())
            self.wfile.write("#CMD#US|3;{}@{}#END#\n".format(b_dist, str(timestamp)).encode())
            time.sleep(.5)
            print("Ultrasonic Sensor Values has been sent.")

    def handle(self):
        if self.cmd_handler is None:
            self.initiate()
        while True:
            self.data = self.rfile.readline().strip()
            if not self.data:
                break
            # print("raw_data", self.data)
            self.data = self.data.decode()
            if self.data != "" and not self.distance_interrupt:
                cmd = commands.Command(command_string=self.data)
                self.cmd_handler.addCommand(cmd)
                movementCommand = self.cmd_handler.lastCommand(commands.COMMAND_TYPE_AUTOPILOT)
                if movementCommand is not None and movementCommand.type == commands.COMMAND_TYPE_AUTOPILOT:
                    direction = movementCommand.arguments[-1]
                    current_direction = self.steering_motor.current_direction()
                    if direction == "FORWARD":
                        print("Direction(Must be):", direction)
                    elif direction == "LEFT":
                        print("Direction(Must be):", direction)
                    elif direction == "RIGHT":
                        print("Direction(Must be):", direction)

                    if direction == "FORWARD":
                        # self.steering_motor.stop()
                        self.steering_motor.forward_dir()
                        self.motor.forward(speed = 50)
                    elif direction == "RIGHT":
                        # self.steering_motor.stop()
                        self.steering_motor.right()
                    elif direction == "LEFT":
                        # self.steering_motor.stop()
                        self.steering_motor.left()
                    elif direction == "STOP":
                        self.motor.stop()
                        self.steering_motor.forward_dir()
                        self.steering_motor.stop()
                if movementCommand is not None and movementCommand.type == commands.COMMAND_TYPE_MOVEMENT_CONTROL:
                    yaxis = int(movementCommand.arguments[1])
                    xaxis = int(movementCommand.arguments[0])
                    if xaxis > 50:
                        self.steering_motor.right()
                    elif xaxis < 50:
                        self.steering_motor.left()
                    else:
                        self.steering_motor.stop()
                    if yaxis > 50:
                        self.motor.forward(speed=50)
                    elif yaxis < 50:
                        self.motor.backward(speed=50)
                    else:
                        self.motor.stop()

                    print("Movement Control data:", self.data, " xaxis:", xaxis, "yaxis:", yaxis)
                    #self.wfile.write(("%s %s\n" % (xaxis, yaxis)).encode())
        self.get_measurement = False
        self.steering_motor.cleanup()
        self.motor.cleanup()
        self.rightw_button.cleanup()
        self.leftw_button.cleanup()
        self.forwardw_button.cleanup()
