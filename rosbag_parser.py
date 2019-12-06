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


	#Multirover Test
	testtitle = 'Multiple Rovers'
	filenames = ['alldata.bag']
	path = '/home/magicc/rtk_tests/tworoveronecomp/'
	bagtitles = ['Data']
	names = ['base', 'rover', 'rover2']

	multiroverbags = []

	for filename in filenames:
		multiroverbags.append(rosbag.Bag(path + filename))

	#Execute function to plot data from rosbags

	multirotor_stdev = parserplot(testtitle, multiroverbags, bagtitles, names, path)

	# testtitle = 'Stationary Base and Rover'
	# filenames = ['rover_northsouth.bag', 'rover_eastwest.bag', 'rover_diagonal.bag']
	# bagtitles = ['Stationary Base Rover Test 1','Stationary Base Rover Test 2', 'Stationary Base Rover Test 3']

	#stationary_base_roverbags = []

	#for filename in filenames:
	#	stationary_base_roverbags.append(rosbag.Bag('/home/matt/data/rtk_tests/stationary-base-rover/'
	#	 + filename))

	#stationary_stdev = parserplot(testtitle, stationary_base_roverbags, bagtitles)

	print(multirotor_stdev)
	#print(stationary_stdev)
	#plt.close('all')

def parserplot(testtitle, rosbags, bagtitles, names, path):

	data = Parser();

	figures = []

	stddevnorth = 0
	stddeveast = 0
	stddevup = 0
	stddevvelnorth = 0
	stddevveleast = 0
	stddevvelup = 0

	bag = rosbags[0];

	index = 0
	#Create a for loop to go through all bags
	for name in names:

		#Get variables from the bag
		variables = data.get_variables(bag, name = name)
		#set_trace();

		#Create blank arrays for Rel Position NED Values
		north = []
		east = []
		up = []
		time = []
		relposheading = []

		#print(variables.relPosNED)


		#Find the flags
		flags = variables.flags

		#Get Relative Position NED Values
		for i in range(0, len(flags)):

			north.append(variables.relPosNED[i][0])
			east.append(variables.relPosNED[i][1])
			up.append(-1.0*variables.relPosNED[i][2])
			relposheading.append(variables.relPosHeading[i])
			timestamp = (variables.secs_rel[i]-variables.secs_rel[0] +
				 (variables.nsecs_rel[i]-variables.nsecs_rel[0])*10.0**(-9))
			if timestamp < 0:
				pass
			else:
				time.append(timestamp)
		#print(north)



		#Create blank arrays for velNED
		#print(time)
		velnorth = []
		veleast = []
		velup = []
		temp = variables.sec
		veltime = []
		startsec = variables.sec[0]


		#Find velNED
		for i in range(0, len(temp)):

			timestamp = ((variables.minute[i] - variables.minute[0])*60 +
				(variables.sec[i] - startsec) +
			    (variables.nano[i]-variables.nano[0])*10**(-9))
			if timestamp < 0:
				pass
			else:
				veltime.append(timestamp)
				velnorth.append(variables.velNED[i][0])
				veleast.append(variables.velNED[i][1])
				velup.append(-1.0*variables.velNED[i][2])

		#Flags
		"""figureflags = plt.figure()
		figureflags.suptitle(name + ' Flags')
		plt.xlabel('Time (sec)')
		plt.ylabel('Flag')
		#plt.axis([0,time[len(flags)-1], 0, stat.mean(flags) + stat.stdev(flags)])
		plt.scatter(time, flags)
		plt.savefig(path+name+'flags.png')
		#set_trace()
		#plt.legend()

		#North Position
		figurenorth = plt.figure()
		figurenorth.suptitle(name + ' North Position')
		plt.xlabel('Time (sec)')
		plt.ylabel('North (m)')
		plt.axis([0, time[len(time)-1], stat.mean(north)-2*stat.stdev(north),
			stat.mean(north)+2*stat.stdev(north)])
		plt.scatter(time, north, 1, label = 'Data')
		plt.plot(time, [stat.mean(north)]*len(time), 'r--', label = 'Mean Average: %.3f meters' %stat.mean(north))
		plt.plot(time, [stat.mean(north)-stat.stdev(north)]*len(time), 'g--', label = 'Standard Deviation: %.3f meters' %stat.stdev(north))
		plt.plot(time, [stat.mean(north)+stat.stdev(north)]*len(time), 'g--')
		plt.legend()
		plt.savefig(path+name+'northpos.png')

		#East Position
		figureeast = plt.figure()
		figureeast.suptitle(name + ' East Position')
		plt.xlabel('Time (sec)')
		plt.ylabel('East (m)')
		plt.axis([0, time[len(time)-1], stat.mean(east)-2*stat.stdev(east),
			stat.mean(east)+2*stat.stdev(east)])
		plt.scatter(time, east, 1, label = 'Data')
		plt.plot(time, [stat.mean(east)]*len(time), 'r--', label = 'Mean Average: %.3f meters' %stat.mean(east))
		plt.plot(time, [stat.mean(east)-stat.stdev(east)]*len(time), 'g--', label = 'Standard Deviation: %.3f meters' %stat.stdev(east))
		plt.plot(time, [stat.mean(east)+stat.stdev(east)]*len(time), 'g--')
		plt.legend()
		plt.savefig(path+name+'eastpos.png')

		#Up Position
		figureup = plt.figure()
		figureup.suptitle(name + ' Vertical Position')
		plt.xlabel('Time (sec)')
		plt.ylabel('Up')
		plt.axis([0, time[len(time)-1], stat.mean(up)-2*stat.stdev(up),
			stat.mean(up)+2*stat.stdev(up)])
		plt.scatter(time, up, 1, label = 'Data')
		plt.plot(time, [stat.mean(up)]*len(time), 'r--', label = 'Mean Average: %.3f meters' %stat.mean(up))
		plt.plot(time, [stat.mean(up)-stat.stdev(up)]*len(time), 'g--', label = 'Standard Deviation: %.3f meters' %stat.stdev(up))
		plt.plot(time, [stat.mean(up)+stat.stdev(up)]*len(time), 'g--')
		plt.legend()
		plt.savefig(path+name+'vertpos.png')

		#North Velocity
		figurevelnorth = plt.figure()
		figurevelnorth.suptitle(name + ' North Velocity')
		plt.xlabel('Time (sec)')
		plt.ylabel('North Velocity (m/s)')
		plt.axis([0, veltime[len(veltime)-1], stat.mean(velnorth)-2*stat.stdev(velnorth),
			stat.mean(velnorth)+2*stat.stdev(velnorth)])
		plt.scatter(veltime, velnorth, 1, label = 'Data')
		plt.plot(veltime, [stat.mean(velnorth)]*len(veltime), 'r--', label = 'Mean Average: %.3f m/s' %stat.mean(velnorth))
		plt.plot(veltime, [stat.mean(velnorth)-stat.stdev(velnorth)]*len(veltime), 'g--', label = 'Standard Deviation: %.3f m/s' %stat.stdev(velnorth))
		plt.plot(veltime, [stat.mean(velnorth)+stat.stdev(velnorth)]*len(veltime), 'g--')
		plt.legend()
		plt.savefig(path+name+'northvel.png')

		#East Velocity
		figureveleast = plt.figure()
		figureveleast.suptitle(name + ' East Velocity')
		plt.xlabel('Time (sec)')
		plt.ylabel('East Velocity (m/s)')
		plt.axis([0, veltime[len(veltime)-1], stat.mean(veleast)-2*stat.stdev(veleast),
			stat.mean(veleast)+2*stat.stdev(veleast)])
		plt.scatter(veltime, veleast, 1, label = 'Data')
		plt.plot(veltime, [stat.mean(veleast)]*len(veltime), 'r--', label = 'Mean Average: %.3f m/s' %stat.mean(veleast))
		plt.plot(veltime, [stat.mean(veleast)-stat.stdev(veleast)]*len(veltime), 'g--', label = 'Standard Deviation: %.3f m/s' %stat.stdev(veleast))
		plt.plot(veltime, [stat.mean(veleast)+stat.stdev(veleast)]*len(veltime), 'g--')
		plt.legend()
		plt.savefig(path+name+'eastvel.png')

		#Up Velocity
		figurevelup = plt.figure()
		figurevelup.suptitle(name + ' Vertical Velocity')
		plt.xlabel('Time (sec)')
		plt.ylabel('Vertical Velocity (m/s)')
		plt.axis([0, veltime[len(veltime)-1], stat.mean(velup)-2*stat.stdev(velup),
			stat.mean(velup)+2*stat.stdev(velup)])
		plt.scatter(veltime, velup, 1, label = 'Data')
		plt.plot(veltime, [stat.mean(velup)]*len(veltime), 'r--', label = 'Mean Average: %.3f m/s' %stat.mean(velup))
		plt.plot(veltime, [stat.mean(velup)-stat.stdev(velup)]*len(veltime), 'g--', label = 'Standard Deviation: %.3f m/s' %stat.stdev(velup))
		plt.plot(veltime, [stat.mean(velup)+stat.stdev(velup)]*len(veltime), 'g--')
		plt.legend()
		plt.savefig(path+name+'vertvel.png')"""

		figurerelposheading = plt.figure()
		figurerelposheading.suptitle(name + ' Relative Position Heading')
		plt.xlabel('Time (sec)')
		plt.ylabel('Heading (Radians)')
		plt.axis([0, time[len(time)-1], stat.mean(relposheading)-2*stat.stdev(relposheading),
			stat.mean(relposheading)+2*stat.stdev(relposheading)])
		plt.scatter(time, relposheading, 1, label = 'Data')
		plt.plot(time, [stat.mean(relposheading)]*len(time), 'r--', label = 'Mean Average: %.3f rad' %stat.mean(relposheading))
		plt.plot(time, [stat.mean(relposheading)-stat.stdev(relposheading)]*len(time), 'g--', label = 'Standard Deviation: %.3f rad' %stat.stdev(relposheading))
		plt.plot(time, [stat.mean(relposheading)+stat.stdev(relposheading)]*len(time), 'g--')
		plt.legend()
		plt.savefig(path+name+'relposheading.png')

		#print(index)
		index = index + 1

		"""stddevnorth = stddevnorth + stat.stdev(north)
		stddeveast = stddeveast + stat.stdev(east)
		stddevup = stddevup + stat.stdev(up)
		stddevvelnorth = stddevvelnorth + stat.stdev(velnorth)
		stddevveleast = stddevveleast + stat.stdev(veleast)
		stddevvelup = stddevvelup + stat.stdev(velup)"""
		plt.show();
		#set_trace()
		plt.close('all')

		#figures.extend([figureflags, figurenorth, figureeast, figureup, figurevelnorth,
	          #figureveleast, figurevelup])

	#Cycle through all the rosbags to get all the data.
	#for rosbag in rosbags:
	stddevnorth = 0
	stddeveast = 0
	stddevup = 0
	stddevvelnorth = 0
	stddevveleast = 0
	stddevvelup = 0


	stddevnorth = stddevnorth/index
	stddeveast = stddeveast/index
	stddevup = stddevup/index
	stddevvelnorth = stddevvelnorth/index
	stddevveleast = stddevveleast/index
	stddevvelup = stddevvelup/index

	return [stddevnorth, stddeveast, stddevup, stddevvelnorth, stddevveleast, stddevvelup]


class Parser:
	def get_variables(self, bag, filename ='', name = 'rover'):

		relPosNED = []
		relPosNEDHP = []
		relPosLength = []
		relPosHPLength = []
		relPosHeading=[]
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
		velNED = [] #NED Velocity (m/s)

		# set_trace()
		for topic, msg, t in bag.read_messages(topics=['/'+name+'/RelPos']):
			relPosNED.append(msg.relPosNED)
			relPosNEDHP.append(msg.relPosHPNED)
			relPosLength.append(msg.relPosLength)
			relPosHPLength.append(msg.relPosHPLength)
			flags.append(msg.flags)
			secs_rel.append(msg.header.stamp.secs)
			nsecs_rel.append(msg.header.stamp.nsecs)
			relPosHeading.append(msg.relPosHeading)

		for topic, msg, t in bag.read_messages(topics=['/'+name+'/PosVelTime']):
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
			velNED.append(msg.velNED)

		for topic, msg, t in bag.read_messages(topics=['/'+name+'/PosVelEcef']):
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
		relPosHeading, flags, secs_rel, nsecs_rel, secs_pos, nsecs_pos, lla, year, month, day, hour, \
		minute, sec, nano, position, meanXYZ, velNED")

		variables = MyStruct(relPosNED, relPosNEDHP, relPosLength, relPosHPLength, \
		relPosHeading, flags, secs_rel, nsecs_rel, secs_pos, nsecs_pos, lla, year, month, day, hour, \
		minute, sec, nano, position, meanXYZ, velNED)

		return variables

if __name__ == '__main__':
    variables = main()
