from RPi import GPIO
import time

GPIO.setmode(GPIO.BCM) # set gpio pin mode to BCM

TRIG_PIN = 17
ECHO_PIN = 27
SOUND_SPEED = 343 # 343 m/s speed of the sound at sea level.

print "Distance measurmenet in progress.."

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

GPIO.output(TRIG_PIN, False)

print "Waiting for sensor.."
time.sleep(2)

GPIO.output(TRIG_PIN, True)

time.sleep(0.00001)

GPIO.output(TRIG_PIN, False) # now ultrasonic sensor sends the sound so we need to listen echo pin's value

while GPIO.input(ECHO_PIN) == 0:
    start_time = time.time()

while GPIO.input(ECHO_PIN) == 1:
    end_time = time.time()

pulse_duration = end_time - start_time

# speed = distance / time ==> speed x time = distance
distance_in_meter = SOUND_SPEED * (pulse_duration / 2)

distance_in_cm = distance_in_meter * 100

# rounding the distance value into 2 decimal places
rounded_distance_in_cm = round(distance_in_cm, 2)

print "Distance: ", rounded_distance_in_cm

GPIO.cleanup()
