#!/usr/bin/python2

import serial, binascii

# Check device TTY and baud rate before deployment to ensure match with Arduino connection
arduino = serial.Serial('/dev/ttyACM0', 9600)

def read_arduino():
	try: 
		str = arduino.readline()
		pairs = str.decode('ascii').split(', ')
	except e:
		print ('No go on data read.')
		return False
	data = {}
	i=0
	for a in pairs :
		item = a.split(': ')
		if len(item) < 2 :
			data[item[0]] = "NULL"
		else :
			data[item[0]] = item[1]
		i = i + 1
	return data
	
#def write_arduino(cmdstr)
#	arduino.write(cmdstr)
	

#Test output	
while True:
	data = read_arduino()
	if data != False :
		for k,v in data.items():
			print (k, " -- ", v)

	
	