#be sure to specify filename in this file
from IPython.core.debugger import set_trace
import rosbag
import pickle
from collections import namedtuple

def main():

	filename = 'land_2-19.bag'
	bag = rosbag.Bag('../../data/mocap/' + filename)
	data = Parser()
	variables = data.get_variables(bag)
	bag.close()
	return variables

class Parser:
	def get_variables(self, bag):

		plt_sec = []
		plt_nsec = []
		plt_x = []
		plt_y = []
		plt_z = []
		plt_orientation = []

		plt_virt_sec = []
		plt_virt_nsec = []
		plt_virt_x = []
		plt_virt_y = []
		plt_virt_z = []
		plt_virt_orientation = []

		drone_sec = []
		drone_nsec = []
		drone_x = []
		drone_y = []
		drone_z = []
		drone_orientation = []

		hl_comd_sec = []
		hl_comd_nsec = []
		hl_comd_x = []
		hl_comd_y = []
		hl_comd_z = []
		hl_comd_orientation = []

		is_flying = []

		is_landing = []

		odom_sec = []
		odom_nsec = []
		odom_x = []
		odom_y = []
		odom_z = []
		odom_orientation = []

		for topic, msg, t in bag.read_messages(topics=['/boat_landing_platform_ned']): #this is the estimate
			plt_sec.append(msg.header.stamp.secs)
			plt_nsec.append(msg.header.stamp.nsecs)			
			plt_x.append(msg.pose.position.x)
			plt_y.append(msg.pose.position.y)
			plt_z.append(msg.pose.position.z)
			plt_pos = [plt_x, plt_y, plt_z]
			plt_orientation.append(msg.pose.orientation)
			plt = pos_orient_time(plt_sec, plt_nsec, plt_x, plt_y, plt_z, plt_orientation)

		for topic, msg, t in bag.read_messages(topics=['/platform_virtual_odometry']): #this is the estimate
			plt_virt_sec.append(msg.header.stamp.secs)
			plt_virt_nsec.append(msg.header.stamp.nsecs)			
			plt_virt_x.append(msg.pose.pose.position.x)
			plt_virt_y.append(msg.pose.pose.position.y)
			plt_virt_z.append(msg.pose.pose.position.z)
			plt_virt_pos = [plt_virt_x, plt_virt_y, plt_virt_z]
			plt_virt_orientation.append(msg.pose.pose.orientation)
			plt_virt = pos_orient_time(plt_virt_sec, plt_virt_nsec, plt_x, plt_y, plt_z, plt_virt_orientation)


		for topic, msg, t in bag.read_messages(topics=['/ragnarok_ned']): #this is the estimate
			drone_sec.append(msg.header.stamp.secs)
			drone_nsec.append(msg.header.stamp.nsecs)			
			drone_x.append(msg.pose.position.x)
			drone_y.append(msg.pose.position.y)
			drone_z.append(msg.pose.position.z)
			drone_pos = [drone_x, drone_y, drone_z]
			drone_orientation.append(msg.pose.orientation)
			drone = pos_orient_time(drone_sec, drone_nsec, plt_x, plt_y, plt_z, drone_orientation)

		for topic, msg, t in bag.read_messages(topics=['/high_level_command']): #this is the estimate
			hl_comd_sec.append(msg.header.stamp.secs)
			hl_comd_nsec.append(msg.header.stamp.nsecs)			
			hl_comd_x.append(msg.x)
			hl_comd_y.append(msg.y)
			hl_comd_z.append(msg.z)
			hl_comd_pos = [hl_comd_x, hl_comd_y, hl_comd_z]
			hl_comd_orientation.append(msg.F)
			hl_comd = pos_orient_time(hl_comd_sec, hl_comd_nsec, plt_x, plt_y, plt_z, hl_comd_orientation)

		for topic, msg, t in bag.read_messages(topics=['/is_flying']): #this is the estimate
			is_flying.append(msg.data)

		for topic, msg, t in bag.read_messages(topics=['/is_landing']): #this is the estimate
			is_landing.append(msg.data)

		for topic, msg, t in bag.read_messages(topics=['/odom']): #this is the estimate
			odom_sec.append(msg.header.stamp.secs)
			odom_nsec.append(msg.header.stamp.nsecs)			
			odom_x.append(msg.pose.pose.position.x)
			odom_y.append(msg.pose.pose.position.y)
			odom_z.append(msg.pose.pose.position.z)
			odom_pos = [odom_x, odom_y, odom_z]
			odom_orientation.append(msg.pose.pose.orientation)
			odom = pos_orient_time(odom_sec, odom_nsec, plt_x, plt_y, plt_z, odom_orientation)

		MyStruct = namedtuple("mystruct", "plt, plt_virt, drone, hl_comd, is_flying, is_landing, odom")

		variables = MyStruct(plt, plt_virt, drone, hl_comd, is_flying, is_landing, odom)

		return variables

class pos_orient_time:
	def __init__(self, sec, nsec, x, y, z, orientation):
		self.time = sec+nsec*1E-9
		self.position = [x, y, z]
		self.orientation = orientation

if __name__ == '__main__':
    variables = main()
