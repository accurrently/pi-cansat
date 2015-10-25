#!/usr/bin/python2

# This file has functions for interfacing with an Arduino board via USB

# Get our libs
import serial;
import binascii;
import time;
import io;

# When changing your data being sent by Arduino, be sure to change these headers.
# This is hacky for now, but is cheaper in terms of memory than JSON, 
# since Arduino only has so much memory to work with.


# Headers for data columns
PCS_DATA_HEADERS = 'timestamp,temperature,humidity,pressure,pTemperature,accelX,accelY,accelZ,magX,magY,magZ,latitude,longitude,altitude,speed\n'

# Abbreviations for headers
PCS_DATA_KEYS = ['t', 'h', 'p', 'pt', 'ax', 'ay', 'az', 'mx', 'my', 'mz', 'lat', 'lon', 'alt', 'speed']

# Check device TTY and baud rate before deployment to ensure match with Arduino connection
arduino = serial.Serial('/dev/ttyACM0', 9600)

# Listen to Arduino and get data from sensors
def pcs_getdata():
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

# Test output
def pcs_arduino_test():
	while True:
		data = pcs_getdata()
		if data != False :
			for k,v in data.items():
				print (k, " -- ", v)
				
# Use for filling rows with NULL data
def pcs_fillnull():
	i = 0
	out = ''
	while i < len(PCS_DATA_HEADERS.split(',')) :
		out += 'NULL'
		if i < len(PCS_DATA_HEADERS.split(',')) - 1 :
			out += ','
		i = i + 1
	return out
	
		
# Logs sensor data and outputs to CSV
def pcs_logdatacsv():
	out = PCS_DATA_HEADERS
	start = time.time()
	while time.time() - start < 60 :
		failures = 0
		line = ''
		data = pcs_getdata()
		stamp = time.ctime()
		if data == False :
			line += pcs_fillnull()
		else :
			i = 0
			while i < len(PCS_DATA_KEYS) :
				if PCS_DATA_KEYS[i] in data:
					line += data[PCS_DATA_KEYS[i]]
				else :
					failures = failures + 1
					line += 'NULL'
				if i < len(PCS_DATA_KEYS) - 1 :
					line += ','
				i = i + 1
			#line += '\n'
			if failures <= 6 :
				print ('[[', time.time() - start, ' of 60 sec]] ', stamp, ',', line)
				out += stamp
				out += ','
				out +=  line
			else:
				print ('NO GOOD DATA')			
	f = open('satdata.csv', 'w+')
	f.write(out)
	f.close()
	
	

	
	