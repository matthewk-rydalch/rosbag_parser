#be sure to specify filename in this file
from IPython.core.debugger import set_trace
import rosbag
import pickle
from collections import namedtuple

def main():

	filename = 'rover_binary.bag'
	bag = rosbag.Bag('../../../data/rtk_tests/altitude/' + filename)
	# bag = rosbag.Bag(filename)
	# foldername = 'redo_rod/one/'
	# bag = rosbag.Bag('../../../data/' + foldername + 'data_fixed.bag')
	data = Parser()
	# variables = data.get_varaibles(bag, foldername)
	variables = data.get_variables(bag, filename)
	bag.close()
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
			# relPosNEDHP.append(msg.relPosHPNED)
			relPosLength.append(msg.relPosLength)
			# relPosHPLength.append(msg.relPosHPLength)
			flags.append(msg.flags)
			secs_rel.append(msg.header.stamp.secs)
			nsecs_rel.append(msg.header.stamp.nsecs)

		for topic, msg, t in bag.read_messages(topics=['/base/PosVelTime']):
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

		MyStruct = namedtuple("mystruct", "relPosNED, relPosLength, \
		flags, sec_rel, nsec_rel, sec_pos, nsec_pos, lla, year, month, day, hour, \
		minute, sec, nano, position, meanXYZ")
		# MyStruct = namedtuple("mystruct", "relPosNED, relPosNEDHP, relPosLength, relPosHPLength, \
		# flags, sec_rel, nsec_rel, sec_pos, nsec_pos, lla, year, month, day, hour, \
		# minute, sec, nano, position, meanXYZ")

		# variables = MyStruct(relPosNED, relPosNEDHP, relPosLength, relPosHPLength, \
		# flags, secs_rel, nsecs_rel, secs_pos, nsecs_pos, lla, year, month, day, hour, \
		# minute, sec, nano, position, meanXYZ)
		variables = MyStruct(relPosNED, relPosNED, relPosLength, relPosLength, \
		flags, secs_rel, nsecs_rel, secs_pos, nsecs_pos, lla, year, month, day, hour, \
		minute, sec, nano, position, meanXYZ)

		return variables

if __name__ == '__main__':
    variables = main()
