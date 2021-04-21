import sys
sys.path.append('../')

from rosbag_parser import Parser
from controller import Controller
import matplotlib.pyplot as plt
# from IPython.core.debugger import set_trace
import rosbag
import numpy as np
from collections import namedtuple

def main():
	data = Parser()
	filename = 'landing_ublox2.bag'
	bag = rosbag.Bag('../../../data/outdoor/flights_0203/' + filename)

	odom, hlc, pos_cmd = get_data(data, bag)

	control = Controller(odom, hlc, pos_cmd.time[0])
	control.run_controller()
	show_north_data(odom.time,odom.position[0],hlc.time,hlc.position[0],pos_cmd,control.nPID.command,control.time)
	show_east_data(odom.time,odom.position[1],hlc.time,hlc.position[1],pos_cmd,control.ePID.command,control.time)
	show_down_data(odom.time,odom.position[2],hlc.time,hlc.position[2],pos_cmd,control.dPID.command,control.time)
	show_integrator(odom.time,odom.position[1],hlc.time,hlc.position[1],control.ePID.integrator,control.time)

	plt.show()

def get_data(data, bag):

	odom = data.get_odom(bag)
	hlc = data.get_high_level_command(bag)
	pos_cmd = data.get_roscop_pos_cmd(bag)
	# vel_cmd = data.get_roscop_vel_cmd(bag)

	bag.close()

	return odom, hlc, pos_cmd


def show_north_data(odom_time,odom,hlc_time,hlc,actual,expected,expected_time):
	fig_num = 1
	plot_2_subplots(fig_num, odom_time, odom, 'odom', hlc_time, hlc, 'hlc', actual.time, actual.x, 'actual', expected_time, expected, 'expected')

def show_east_data(odom_time,odom,hlc_time,hlc,actual,expected,expected_time):
	fig_num = 2
	plot_2_subplots(fig_num, odom_time, odom, 'odom', hlc_time, hlc, 'hlc', actual.time, actual.y, 'actual', expected_time, expected, 'expected')

def show_down_data(odom_time,odom,hlc_time,hlc,actual,expected,expected_time):
	fig_num = 3
	plot_2_subplots(fig_num, odom_time, odom, 'odom', hlc_time, -np.array(hlc), 'hlc', actual.time, actual.z, 'actual', expected_time, expected, 'expected')

def show_integrator(odom_time,odom,hlc_time,hlc,expected,expected_time):
	fig_num = 4
	plot_21_subplots(fig_num, odom_time, odom, 'odom', hlc_time, hlc, 'hlc', expected_time, expected, 'expected')

def plot_2(fig_num, t_x, x, xlabel, t_y, y, ylabel):

	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.legend(loc = "upper right")

def plot_3(fig_num, t_x, x, xlabel, t_y, y, ylabel, t_z,z, zlabel):

	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.plot(t_z, z, label = zlabel)
	plt.legend(loc = "upper right")

def plot_2_subplots(fig_num, t_x, x, xlabel, t_y, y, ylabel, t_z,z, zlabel, t_w,w ,wlabel):
	plt.figure(fig_num)
	plt.subplot(211)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.legend(loc = "upper right")
	plt.subplot(212)
	plt.plot(t_z, z, label = zlabel)
	plt.plot(t_w, w, label = wlabel)
	plt.legend(loc = "upper right")

def plot_21_subplots(fig_num, t_x, x, xlabel, t_y, y, ylabel, t_z,z, zlabel):
	plt.figure(fig_num)
	plt.subplot(211)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.legend(loc = "upper right")
	plt.subplot(212)
	plt.plot(t_z, z, label = zlabel)
	plt.legend(loc = "upper right")


if __name__ == '__main__':
	main()
