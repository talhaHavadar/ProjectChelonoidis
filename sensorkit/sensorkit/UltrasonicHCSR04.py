from RPi import GPIO as io
import time

class UltrasonicHCSR04(object):
    """docstring for UltrasonicHCSR04."""

    SOUND_SPEED = 343 # 343 m/s

    def __init__(self, echo_pin, trig_pin, name = "Ultrasonic Sensor"):
        self.echo_pin = echo_pin
        self.trig_pin = trig_pin
        self.is_ready = False
        self.name = name


    def __setup(self):
        print("[-] %s is setting up.." % (self.name))
        io.setmode(io.BCM)
        io.setup(self.trig_pin, io.OUT, initial = io.LOW)
        io.setup(self.echo_pin, io.IN)
        time.sleep(2)
        self.is_ready = True
        print("[-] Setup completed.")

    def getDistance(self, distance_unit = "cm"):
        if distance_unit == "cm":
            distance = self.__getDistance() * 100
            return round(distance, 2)
        elif distance_unit == "m":
            return round(self.__getDistance(), 2)
        else:
            # TODO: Throw an exception for unsupported metric unit
            print("Unsupported metric unit")
            return -1

    def getDistanceAvg(self, distance_unit = "cm", measurement_number = 5, sleep = .2):
        if sleep < .2:
            raise ValueError("sleep must be bigger than 0.2")
        measurement_number = int(measurement_number)
        if measurement_number == 0:
            raise ValueError("measurement_number must be bigger than 0")
        measurements = list()
        for i in range(measurement_number):
            measurements.append(self.getDistance(distance_unit))
            time.sleep(sleep)
        return round((sum(measurements) / len(measurements)), 2)

    """
        cleans trigger and echo pins.
    """
    def cleanup(self):
        io.cleanup((self.trig_pin, self.echo_pin))

    """
        returns distance from an object in meters
    """
    def __getDistance(self):
        if not self.is_ready:
            self.__setup()
        start_time = -1
        end_time = -1
        io.output(self.trig_pin, True)
        time.sleep(0.00001) # wait for 10uS
        io.output(self.trig_pin, False) # now ultrasonic sensor sends the sound so we need to listen echo pin's value

        while io.input(self.echo_pin) == 0:
            start_time = time.time()

        while io.input(self.echo_pin) == 1:
            end_time = time.time()

        pulse_duration = end_time - start_time
        # speed = distance / time ==> speed x time = distance
        return self.SOUND_SPEED * (pulse_duration / 2)
