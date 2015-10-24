#!/usr/bin/python

import serial

# Check device TTY and baud rate before deployment to ensure match with Arduino connection
arduino = serial.Serial('/dev/ttyACM0', 9600)

def read_arduino():
	str = arduino.readline()
	pairs = str.split(', ')
	data = {}
	for pair in pairs :
		item = pair.split(': ')
		data[item[0]] = item[1]
	return data
	
def write_arduino(cmdstr)
	arduino.write(cmdstr)
	


	
	