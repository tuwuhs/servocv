

import cv2
import serial
import msvcrt
from serial.tools import list_ports

s = serial.Serial()
s.port = list_ports.grep('067B:2303').next()[0]
s.baudrate = 115200
s.bytesize = serial.EIGHTBITS
s.parity = serial.PARITY_NONE
s.stopbits = serial.STOPBITS_ONE
s.open()

keypress = ''
servopos = 0
s.write('(s0 %d)' % servopos)
while(keypress != 'q'):
	keypress = msvcrt.getch()
	if keypress == 'h':
		servopos = max(servopos-500, -10000)
		s.write('(s0 %d)' % servopos)
	elif keypress == 'l':
		servopos = min(servopos+500, 10000)
		s.write('(s0 %d)' % servopos)

s.close()