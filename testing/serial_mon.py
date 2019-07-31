import serial
from time import sleep
from serial import Serial

while(True):

	with Serial('/dev/ttyACM0', 9600, timeout=1) as ser:
		x = ser.read()          # read one byte
		s = ser.read(256)        # read up to ten bytes (timeout)
		line = ser.readline()   # read a '\n' terminated line
		print(line)

	sleep(0.5)