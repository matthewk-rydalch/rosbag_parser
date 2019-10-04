#be sure to specify filename in this file
from IPython.core.debugger import set_trace
import rosbag
import pickle
from collections import namedtuple

def main():

	filename = 'test.bag'
	bag = rosbag.Bag('../../../' + filename)
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

		sec_c = []
		Xc = []
		Yc = []
		Zc = []
		Fc = []

		sec = []
		nsec = []
		X = []
		Y = []
		Z = []
		
		# set_trace()
		for topic, msg, t in bag.read_messages(topics=['/high_level_command']):
			sec_c.append(msg.header.stamp.secs)
			Xc.append(msg.x)
			Yc.append(msg.y)
			Zc.append(msg.z)
			Fc.append(msg.F)

		for topic, msg, t in bag.read_messages(topics=['/multirotor/truth/NED']):
			sec.append(msg.header.stamp.secs)
			nsec.append(msg.header.stamp.nsecs)
			X.append(msg.pose.pose.position.x)
			Y.append(msg.pose.pose.position.y)
			Z.append(msg.pose.pose.position.z)

		MyStruct = namedtuple("mystruct", "sec_c, Xc, Yc, Zc, Fc, \
		sec, nsec, X, Y, Z")

		variables = MyStruct(sec_c, Xc, Yc, Zc, Fc, \
		sec, nsec, X, Y, Z)

		return variables

if __name__ == '__main__':
    variables = main()
