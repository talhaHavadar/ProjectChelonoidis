import socketserver
import socket
import threading
import RPi.GPIO as GPIO
import time
from sensorkit.Servo import TowerProMG995
from sensorkit.UltrasonicHCSR04 import UltrasonicHCSR04


class UDPServerHandler(socketserver.BaseRequestHandler):

    def setup(self):
        print("Client connected ", self.client_address)
        super(UDPServerHandler, self).setup()


    def handle(self):
        self.server.add_client(self.client_address[0])
        data = self.request[0].strip().decode()
        socket = self.request[1]
        print(self.client_address[0],' wrote: ', data)
        command, value = str(data).split('|')
        print(command, command.strip(), command == 'steering')
        if command.strip() == 'steering':
            print("steering", self.server.steering, " angle:",  int(value.strip()))
            self.server.steering.angle = int(value.strip())
        socket.sendto(data.encode().upper(), (self.client_address[0], 7777))


class UDPServer(socketserver.ThreadingUDPServer):
    """UDPServer with broadcasting capability"""

    def __init__(self, server_address, request_handler_class):
        """Initializes a ThreadingUDPServer with clients set"""
        print("Server starting at %s:%s..." % (server_address[0], server_address[1]))
        super(UDPServer,self).__init__(server_address, request_handler_class, True)
        self.clients = set()
        GPIO.setmode(GPIO.BCM)
        print("Servo motor is setting up..")
        self.steering = TowerProMG995(18)
        self.steering.setup()
        self.distance_front = UltrasonicHCSR04(echo_pin=27, trig_pin=17, name="Front Ultrasonic")
        print("Server started")
        self.d_thread = DistanceThread(self)
        self.d_thread.start()

    def add_client(self, client):
        """Registers a client to clients set"""
        self.clients.add(client)

    def broadcast(self, source, data):
        """Sends data to all clients from the source"""
        for client in self.clients:
            if client is not source:
                self.socket.sendto(data.encode(), (client, 7777))

    def remove_client(self, client):
        """Removes clients from the set"""
        self.clients.remove(client)

class DistanceThread(threading.Thread):
    """docstring for DistanceThread."""
    def __init__(self, server: UDPServer):
        super(DistanceThread, self).__init__()
        self.server = server

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            dist = self.server.distance_front.getDistance()
            print("dist_front|" + str(dist))
            s.sendto(("dist_front|" + str(dist)).encode(), ('192.168.1.255', 7777))
            time.sleep(.5)


if __name__ == '__main__':
    HOST, PORT = "192.168.1.1", 7777
    server = UDPServer((HOST,PORT), UDPServerHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        GPIO.cleanup()
