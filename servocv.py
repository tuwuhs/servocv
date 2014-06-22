
import cv2
import serial
import msvcrt
import numpy as np
from serial.tools import list_ports

s = serial.Serial()
s.port = list_ports.grep('067B:2303').next()[0]
s.baudrate = 115200
s.bytesize = serial.EIGHTBITS
s.parity = serial.PARITY_NONE
s.stopbits = serial.STOPBITS_ONE
s.open()

cam = cv2.VideoCapture(1)

keypress = 0
servopos = 0
s.write('(s0 %d)' % servopos)
while(keypress != 27):
	ret, frame = cam.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.blur(gray, (3, 3))
	thresh = 254 # np.amax(gray) * 0.95
	ret, gray = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
	
	contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	
	cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)
	
	max_area = 0
	best_contour = None
	for c in contours:
		area = cv2.contourArea(c)
		if area > max_area:
			max_area = area
			best_contour = c
	
	area_threshold = 3000
	if best_contour != None and max_area > area_threshold:
		mom = cv2.moments(best_contour)
		cx, cy = mom['m10']/mom['m00'], mom['m01']/mom['m00']
		cv2.circle(frame, (int(cx), int(cy)), 10, (0, 255, 0), 20)
	cv2.imshow('frame', frame)
	
	keypress = cv2.waitKey(1) & 0xFF
	if keypress == ord('h'):
		servopos = max(servopos-500, -10000)
		s.write('(s0 %d)' % servopos)
	elif keypress == ord('l'):
		servopos = min(servopos+500, 10000)
		s.write('(s0 %d)' % servopos)

cam.release()
cv2.destroyAllWindows()
s.close()