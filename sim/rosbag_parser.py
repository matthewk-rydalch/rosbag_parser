#be sure to specify filename in this file
from IPython.core.debugger import set_trace
import rosbag
import pickle
from collections import namedtuple

def main():

	filename = '10-22-19.bag.active'
	bag = rosbag.Bag('../../data/boatLanding_sim/' + filename)
	# bag = rosbag.Bag(filename)
	# foldername = 'redo_rod/one/'
	# bag = rosbag.Bag('../../../data/' + foldername + 'data_fixed.bag')
	data = Parser()
	# variables = data.get_varaibles(bag, foldername)
	variables = data.get_variables(bag)
	bag.close()
	return variables

class Parser:
	def get_variables(self, bag):

		gnss_sec = []
		gnss_nsec = []
		gnss_pos = []

		odom_sec = []
		odom_nsec = []
		odom_x = []
		odom_y = []
		odom_z = []
		odom_orientation = []

		ned_sec = []
		ned_nsec = []
		ned_pos = []
		ned_orientation = []

		thr_sec = []  #throttled NED or truth
		thr_nsec = []
		thr_pos = []
		thr_x = []
		thr_y = []
		thr_z = []
		thr_orientation = []

		wp_sec = []
		wp_nsec = []
		wp_x = []
		wp_y = []
		wp_z = []

		# # set_trace()
		# for topic, msg, t in bag.read_messages(topics=['/multirotor/gps/data']):
		# 	gnss_sec.append(msg.header.stamp.secs)
		# 	gnss_nsec.append(msg.header.stamp.nsecs)
		# 	gnss_pos.append(msg.position)

		for topic, msg, t in bag.read_messages(topics=['/multirotor/odom']): #this is the estimate
			odom_sec.append(msg.header.stamp.secs)
			odom_nsec.append(msg.header.stamp.nsecs)			
			odom_x.append(msg.pose.pose.position.x)
			odom_y.append(msg.pose.pose.position.y)
			odom_z.append(msg.pose.pose.position.z)
			odom_pos = [odom_x, odom_y, odom_z]
			odom_orientation.append(msg.pose.pose.orientation)

		# for topic, msg, t in bag.read_messages(topics=['/multirotor/ground_truth/odometry/NED']):
		# 	ned_sec.append(msg.header.stamp.secs)
		# 	ned_nsec.append(msg.header.stamp.nsecs)			
		# 	ned_pos.append(msg.pose.pose.position)
		# 	ned_orientation.append(msg.pose.pose.orientation)

		for topic, msg, t in bag.read_messages(topics=['/multirotor/ground_truth/odometry/NED_throttled']): #this is the actual
			thr_sec.append(msg.header.stamp.secs)
			thr_nsec.append(msg.header.stamp.nsecs)			
			thr_x.append(msg.pose.pose.position.x)
			thr_y.append(msg.pose.pose.position.y)
			thr_z.append(msg.pose.pose.position.z)
			thr_pos = [thr_x, thr_y, thr_z]
			thr_orientation.append(msg.pose.pose.orientation)

		for topic, msg, t in bag.read_messages(topics=['/multirotor/high_level_command']):
			wp_sec.append(msg.header.stamp.secs)
			wp_nsec.append(msg.header.stamp.nsecs)
			wp_x.append(msg.x)
			wp_y.append(msg.y)
			wp_z.append(msg.F) #mislabeled in roscopter?

		MyStruct = namedtuple("mystruct", "odom_sec, odom_nsec, odom_pos, odom_orientation, \
		thr_sec, thr_nsec, thr_pos, thr_orientation, wp_sec, wp_nsec, wp_x, wp_y, wp_z")

		variables = MyStruct(odom_sec, odom_nsec, odom_pos, odom_orientation, thr_sec, \
		thr_nsec, thr_pos, thr_orientation, wp_sec, wp_nsec, wp_x, wp_y, wp_z)


		return variables

if __name__ == '__main__':
    variables = main()
