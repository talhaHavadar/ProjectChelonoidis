from socket import *
import time
s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
count = 0
while True:
	count = count + 1
	s.sendto('this is from raspberry pi %s' % count, ('192.168.1.255', 7777))
	time.sleep(.8)
