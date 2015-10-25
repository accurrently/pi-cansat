#!/usr/bin/python2

import serial;
import binascii;
import time;
import io;

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
def arduino_test():
	while True:
		data = read_arduino()
		if data != False :
			for k,v in data.items():
				print (k, " -- ", v)
				
def arduino_log():
	out = 'timestamp,temperature,humidity,pressure,pTemperature,accelX,accelY,accelZ,magX,magY,magZ,latitude,longitude,altitude,speed\n'
	start = time.time()
	while time.time() - start < 60 :
		failures = 0
		line = ''
		data = read_arduino()
		stamp = time.ctime()
		if data == False :
			line += 'NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL'
		else :
			keys = ['t', 'h', 'p', 'pt', 'ax', 'ay', 'az', 'mx', 'my', 'mz', 'lat', 'lon', 'alt', 'speed']
			print(keys)
			i = 0
			while i < len(keys) :
				if keys[i] in data:
					#print ('key found: "' , keys[i], '"\n')
					line += data[keys[i]]
				else :
					failures = failures + 1
					#print ('key MISSING: "' , keys[i], '"\n')
					line += 'NULL'
				if i < len(keys) - 1 :
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
	
arduino_log()
	
	

	
	