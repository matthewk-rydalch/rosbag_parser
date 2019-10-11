#be sure to specify filename in this file
from IPython.core.debugger import set_trace
from importlib import reload
import rosbag
import pickle
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
import statistics as stat

def main():

	

	filename = 'rover-10-4-stationary.bag'
	bag = rosbag.Bag('../rtk_tests/stationary/' + filename)
	# bag = rosbag.Bag(filename)
	# foldername = 'redo_rod/one/'
	# bag = rosbag.Bag('../../../data/' + foldername + 'data_fixed.bag')
	data = Parser()
	# variables = data.get_varaibles(bag, foldername)
	variables = data.get_variables(bag, filename)
	bag.close()

	#for variable_type in variables[0]:
	#	print (%s, variable_type)
	#	for value in variable_type:
	#		print ("%d" %value)

	
	#Create blank arrays for Rel Position NED Values
	north = []
	east = []
	up = []
	time = []

	#Find the flags
	flags = variables.flags

	#Get Relative Position NED Values
	for i in range(0, len(flags)):

		#print(i)
		north.append(variables.relPosNED[i][0])
		east.append(variables.relPosNED[i][1])
		up.append(-1*variables.relPosNED[i][2])
		time.append(variables.secs_rel[i]-variables.secs_rel[0])

	figurenorth = plt.figure()
	figurenorth.suptitle('Stationary Test North')
	plt.xlabel('Time (sec)')
	plt.ylabel('North (m)')
	plt.axis([0, time[len(time)-1], stat.mean(north)-2*stat.stdev(north), 
		stat.mean(north)+2*stat.stdev(north)])
	plt.scatter(time,north, 1, label = 'Data')
	plt.plot(time, [stat.mean(north)]*len(time), 'r--', label = 'Mean Average: %.3f meters' %stat.mean(north))
	plt.plot(time, [stat.mean(north)-stat.stdev(north)]*len(time), 'g--', label = 'Standard Deviation: %.3f meters' %stat.stdev(north))
	plt.plot(time, [stat.mean(north)+stat.stdev(north)]*len(time), 'g--')
	plt.legend()

	figureeast = plt.figure()
	figureeast.suptitle('Stationary Test East')
	plt.xlabel('Time (sec)')
	plt.ylabel('East (m)')
	plt.axis([0, time[len(time)-1], stat.mean(east)-2*stat.stdev(east), 
		stat.mean(east)+2*stat.stdev(east)])
	plt.scatter(time, east, 1, label = 'Data')
	plt.plot(time, [stat.mean(east)]*len(time), 'r--', label = 'Mean Average: %.3f meters' %stat.mean(east))
	plt.plot(time, [stat.mean(east)-stat.stdev(east)]*len(time), 'g--', label = 'Standard Deviation: %.3f meters' %stat.stdev(east))
	plt.plot(time, [stat.mean(east)+stat.stdev(east)]*len(time), 'g--')
	plt.legend()

	figureup = plt.figure()
	figureup.suptitle('Stationary Test Up')
	plt.xlabel('Time (sec)')
	plt.ylabel('Up')
	plt.axis([0, time[len(time)-1], stat.mean(up)-2*stat.stdev(up), 
		stat.mean(up)+2*stat.stdev(up)])
	plt.scatter(time, up, 1, label = 'Data')
	plt.plot(time, [stat.mean(up)]*len(time), 'r--', label = 'Mean Average: %.3f meters' %stat.mean(up))
	plt.plot(time, [stat.mean(up)-stat.stdev(up)]*len(time), 'g--', label = 'Standard Deviation: %.3f meters' %stat.stdev(up))
	plt.plot(time, [stat.mean(up)+stat.stdev(up)]*len(time), 'g--')
	plt.legend()


	#Vertical Test 1

	#Create list containing names of files to parse
	filenames = ["rover-10-4-sliding_post.bag", "rover-10-4-sliding_post_test_2.bag", "rover-10-4-sliding_post_test_3.bag"]

	#Get variables from bag1
	bag1 = rosbag.Bag('../rtk_tests/altitude/' + filenames[0])
	variables1 = data.get_variables(bag1,filenames[0])
	bag1.close()

	#Get variables from bag2
	bag2 = rosbag.Bag('../rtk_tests/altitude/' + filenames[1])
	variables2 = data.get_variables(bag2, filenames[1])
	bag2.close()

	#Get variables from bag3
	bag3 = rosbag.Bag('../rtk_tests/altitude/' + filenames[2])
	variables3 = data.get_variables(bag3, filenames[2])
	bag3.close()

	#Create blank arrays for altitudes for all three tests 
	altitude1 = []
	altitude2 = []
	altitude3 = []

	#Create blank arrays for timestamps
	time1 = []
	time2 = []
	time3 = []

	#Insert altitude and time values from from variables1 into altitude1 and time1
	for i in range(0, len(variables1.flags)):

		#Make Down Up by multiplying by -1
		altitude1.append(-1*variables1.relPosNED[i][2])
		time1.append(variables1.secs_rel[i]-variables1.secs_rel[0])

	#Insert altitude and time values from from variables2 into altitude2 and time2
	for i in range(0, len(variables2.flags)):

		altitude2.append(-1*variables2.relPosNED[i][2])
		time2.append(variables2.secs_rel[i]-variables2.secs_rel[0])


	#Insert altitude and time values from from variables3 into altitude3 and time3
	for i in range(0, len(variables3.flags)):

		altitude3.append(-1*variables3.relPosNED[i][2])
		time3.append(variables3.secs_rel[i]-variables3.secs_rel[0])


	#Plot Test 1
	figure1 = plt.figure()
	figure1.suptitle('Altitude Test 1')
	plt.xlabel('Time (sec)')
	plt.ylabel('Up (m)')
	plt.axis([0, time1[len(time1)-1], 0, 2])
	plt.scatter(time1, altitude1, 1, label = 'Data')
	plt.plot(time1, [.27]*len(time1), 'r--', label = "%.3f meters" %(0.27))
	plt.plot(time1, [1.27]*len(time1), 'g--', label = "%.3f meters" %(1.27))
	plt.plot(time1, [1.95]*len(time1), 'k--', label = "%.3f meters" %(1.95))
	plt.legend()

	#Plot Test 2
	figure2 = plt.figure()
	figure2.suptitle('Altitude Test 2')
	plt.xlabel('Time (sec)')
	plt.ylabel('Up (m)')
	plt.axis([0, time2[len(time2)-1], 0, 2])
	plt.scatter(time2, altitude2, 1, label = 'Data')
	plt.plot(time2, [.27]*len(time2), 'r--', label = "%.3f meters" %(0.27))
	plt.plot(time2, [1.27]*len(time2), 'g--', label = "%.3f meters" %(1.27))
	plt.plot(time2, [1.95]*len(time2), 'k--', label = "%.3f meters" %(1.95))
	plt.legend()

	#Plot Test 3
	figure3 = plt.figure()
	figure3.suptitle('Altitude Test 3')
	plt.xlabel('Time (sec)')
	plt.ylabel('Up (m)')
	plt.axis([0, time3[len(time3)-1], 0, 2])
	plt.scatter(time3, altitude3, 1, label = 'Data')
	plt.plot(time3, [.27]*len(time3), 'r--', label = "%.3f meters" %(0.27))
	plt.plot(time3, [1.27]*len(time3), 'g--', label = "%.3f meters" %1.27)
	plt.plot(time3, [1.95]*len(time3), 'k--', label = "%.3f meters" %1.95)
	plt.legend()

	plt.show()



	return variables

class Parser:
	def get_variables(self, bag, filename):

		relPosNED = []
		relPosNEDHP = []
		relPosLength = []
		relPosHPLength = []
		flags = []
		secs_rel = []
		nsecs_rel = []
		secs_pos = []
		nsecs_pos = []
		lla = []
		position = []
		UTC_sec = []
		UTC_nsec = []
		meanXYZ = []
		year = []
		month = []
		day = []
		hour = []
		minute = []
		sec = []
		nano = []
		# set_trace()
		for topic, msg, t in bag.read_messages(topics=['/rover/RelPos']):
			relPosNED.append(msg.relPosNED)
			relPosNEDHP.append(msg.relPosHPNED)
			relPosLength.append(msg.relPosLength)
			relPosHPLength.append(msg.relPosHPLength)
			flags.append(msg.flags)
			secs_rel.append(msg.header.stamp.secs)
			nsecs_rel.append(msg.header.stamp.nsecs)

		for topic, msg, t in bag.read_messages(topics=['/rover/PosVelTime']):
			secs_pos.append(msg.header.stamp.secs)
			nsecs_pos.append(msg.header.stamp.nsecs)
			lla.append(msg.lla)
			year.append(msg.year)
			month.append(msg.month)
			day.append(msg.day)
			hour.append(msg.hour)
			minute.append(msg.min)
			sec.append(msg.sec)
			nano.append(msg.nano)

		for topic, msg, t in bag.read_messages(topics=['/rover/PosVelEcef']):
			position.append(msg.position);

		for topic, msg, t in bag.read_messages(topics=['/base/SurveyStatus']):
			meanXYZ.append(msg.meanXYZ)

		# for topic, msg, t in bag.read_messages(topics=['/rover/Obs']):
		# 	UTC_sec.append(msg.header.stamp)
			# UTC_nsec.append(msg.header.stamp.nsec)

		# for topic, msg, t in bag.read_messages(topics=['/rover/Ephemeris']):
		# 	position.append(msg.position);

		# for topic, msg, t in bag.read_messages(topics=['/rover/GlonassEphemeris']):
		# 	position.append(msg.position);

		MyStruct = namedtuple("mystruct", "relPosNED, relPosNEDHP, relPosLength, relPosHPLength, \
		flags, secs_rel, secs_pos, nsecs_pos, lla, year, month, day, hour, \
		minute, sec, nano, position, meanXYZ")

		variables = MyStruct(relPosNED, relPosNEDHP, relPosLength, relPosHPLength, \
		flags, secs_rel, secs_pos, nsecs_pos, lla, year, month, day, hour, \
		minute, sec, nano, position, meanXYZ)

		return variables

if __name__ == '__main__':
    variables = main()
