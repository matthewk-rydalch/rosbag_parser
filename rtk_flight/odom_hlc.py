from rosbag_parser import Parser
import matplotlib.pyplot as plt
from IPython.core.debugger import set_trace
import rosbag
import numpy as np
from collections import namedtuple

def main():
	
	data = Parser()

	filename = 'debug.bag'
	bag = rosbag.Bag('../../../data/' + filename)

	# data_type = 'm2u'
	#data_type = 'outdoor'
	data_type = 'sim'
	odom, hlc = get_data(data, bag, data_type)
	get_north_data(odom, hlc)
	get_east_data(odom, hlc)
	get_height_data(odom, hlc)


def get_data(data, bag, data_type):

	if data_type == 'm2u':
	
		odom = data.get_odom(bag)
	
		hlc = data.get_high_level_command(bag) #used for mocap2ublox
		
	elif data_type == 'outdoor':
	
		odom = data.get_odom(bag)		

		hlc = data.get_high_level_command(bag)
	
	elif data_type == 'sim':
	
		odom = data.get_multirotor_odom(bag)

		hlc = data.get_multirotor_high_level_command(bag)
		
	else:
		print('invalid data_type')
	
	bag.close()

	return odom, hlc


def get_north_data(odom, hlc):

	odom_time = odom.time
	odom_n = np.array(odom.position[0])

	hlc_time_points = hlc.time
	hlc_n_points = np.array(hlc.position[0])
	hlc_time, hlc_n = level_hlc_data(hlc_time_points, hlc_n_points)

	error_time, error_n = calc_error(odom_time, odom_n, hlc_time, hlc_n)

	fig_title = 'north odometry, waypoints, and error'
	plot_3_subplots(fig_title, odom_time, odom_n, 'odom', hlc_time, hlc_n, 'wps', error_time, error_n, 'error')


def get_east_data(odom, hlc):

	odom_time = odom.time
	odom_e = np.array(odom.position[1])

	hlc_time_points = hlc.time
	hlc_e_points = np.array(hlc.position[1])
	hlc_time, hlc_e = level_hlc_data(hlc_time_points, hlc_e_points)

	error_time, error_e = calc_error(odom_time, odom_e, hlc_time, hlc_e)

	fig_title = 'east odometry, waypoints, and error'
	plot_3_subplots(fig_title, odom_time, odom_e, 'odom', hlc_time, hlc_e, 'wps', error_time, error_e, 'error')


def get_height_data(odom, hlc):

	odom_time = odom.time
	odom_h = -np.array(odom.position[2])

	hlc_time_points = hlc.time
	hlc_h_points = np.array(hlc.position[2])
	hlc_time, hlc_h = level_hlc_data(hlc_time_points, hlc_h_points)

	error_time, error_h = calc_error(odom_time, odom_h, hlc_time, hlc_h)

	fig_title = 'height odometry, waypoints, and error'
	plot_3_subplots(fig_title, odom_time, odom_h, 'odom', hlc_time, hlc_h, 'wps', error_time, error_h, 'error')


def level_hlc_data(time, pos):

	#function inserts data points just before a change in hlc, so that plots have level lines for the durration of that command
	new_time = []
	new_pos = []
	back_step = 0.001 #this is the time back from a point that we insert a value
	for i in range(len(time)):
		if i == 0:
			new_time.append(time[i])
			new_pos.append(pos[i])
		else:
			new_time.append(time[i]-back_step)
			new_time.append(time[i])
			new_pos.append(pos[i-1])
			new_pos.append(pos[i])
	
	return new_time, new_pos


def calc_error(odom_time, odom, hlc_time, hlc):

	error = []

	i = 0
	j = 0

	#loops through points before the last waypoint
	for j in range(len(hlc)):
		while (odom_time[i] < hlc_time[j]):
			error.append(hlc[j] - odom[i])
			i = i+1

	#this is for the last values after the last waypoint
	for k in range(len(odom)-i):
		error.append(error[i-1])
	
	error_time = odom_time

	return error_time, error


def plot_2(fig_num, t_x, x, xlabel, t_y, y, ylabel):

	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.legend(loc = "upper right")


def plot_3_subplots(title, t_x, x, xlabel, t_y, y, ylabel, t_z, z, zlabel):

	fig, sub = plt.subplots(2)
	fig.suptitle(title)

	sub[0].plot(t_x, x, label = xlabel)
	sub[0].plot(t_y, y, label = ylabel)
	sub[0].legend(loc = "upper right")
	sub[0].set_ylabel('position')

	#compare y
	sub[1].plot(t_z, z, label = zlabel)
	sub[1].legend(loc = "upper right")
	sub[1].set_xlabel('t [s]')
	sub[1].set_ylabel('error')


if __name__ == '__main__':
	main()
