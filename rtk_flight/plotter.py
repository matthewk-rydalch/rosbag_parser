from rosbag_parser import Parser
import matplotlib.pyplot as plt
from IPython.core.debugger import set_trace
import rosbag
import numpy as np
from collections import namedtuple

def main():

	data = Parser()

	filenames = ['process_2.bag', 'process_2p5.bag', 'process_4.bag', \
				 'process_4p5.bag', 'candidate1.bag', \
				 'candidate2.bag', 'candidate3.bag']
	plotnames = ['noise = 2', 'noise = 2.5', 'noise = 4', \
				 'noise = 4.5', 'cand. 1', \
				 'cand. 2', 'cand. 3']
	filepath = '../../../data/process_tests/'
	plot_type = 'compare_odom_gps'
	for i in range(len(filenames)):
		filename = filenames[i]
		bag = rosbag.Bag(filepath + filename)
		if plot_type == 'odom_2d':
			odom_2d_plotter(data,bag, plotnames[i])
		if plot_type == 'compare_odom_gps':
			odomVsgps_plotter(data,bag, plotnames[i])
	if plot_type == 'compare_odom_gps':
		bag = rosbag.Bag(filepath + filename)
		hlc = data.get_multirotor_high_level_command(bag)
		plot_position_1(hlc.position[0], 'hlc n')
		plot_position_1(hlc.position[1], 'hlc e')
		bag.close()


	# filename = 'process_2.bag'
	# bag = rosbag.Bag('../../../data/' + filename)

	# cut_time = False
	# start_time = 25
	# end_time = 50

	# sim_odometry_plotter(data, bag, cut_time, start_time, end_time)
	#sim_error_plotter(data, bag)
	#odometry_plotter(data, bag, cut_time, start_time, end_time)
	# single_odom_plotter(data, bag)
	#accuracy_plotter(data, bag)
	#RelPos_plotter(data, bag)
	# odom_2d_plotter(data,bag)
	# odom_flag_plotter(data,bag)

def odomVsgps_plotter(data, bag, plotname):
	odom = data.get_odom(bag)
	gps = data.get_multirotor_gps(bag)
	bag.close()

	label1 = plotname + ' odom_n'
	label2 = plotname + ' odom_e'
	label3 = plotname + ' gps_n'
	label4 = plotname + ' gps_e'


	plot_position_1(odom.position[0], label1)
	plot_position_1(odom.position[1], label2)
	plot_position_1(gps.n, label3)
	plot_position_1(gps.e, label4)
	


def sim_odometry_plotter(data, bag, cut_time, start_time, end_time):
	plt = data.get_platform_odom(bag)
	plt_virt = data.get_platform_virtual_odometry(bag)
	odom = data.get_multirotor_odom(bag)
	hlc = data.get_multirotor_high_level_command(bag)
	bag.close()

	title = 'simulated odometry comparison'

	plot_compare_position_4(plt, 'plt odom', plt_virt, 'plt virtual odom', odom, 'odom', hlc, 'high level command', cut_time, start_time, end_time, title)

def odometry_plotter(data, bag, cut_time, start_time, end_time):
	plt = data.get_boat_landing_platform_ned(bag)
	plt_virt = data.get_platform_virtual_odometry(bag)
	odom = data.get_odom(bag)
	hlc = data.get_high_level_command(bag)
	bag.close()

	title = 'odometry comparison'

	plot_compare_position_4(plt, 'plt odom', plt_virt, 'plt virtual odom', odom, 'odom', hlc, 'high level command', cut_time, start_time, end_time, title)

def single_odom_plotter(data, bag):
	odom = data.get_odom(bag)
	bag.close()

	title = 'odom'

	plot_position_1( odom.position, 'odom', title)

def RelPos_plotter(data, bag):
	sec, nsec, RP_N, RP_E, RP_D, N_hp, E_hp, D_hp, flag = data.get_RelPos(bag)
	bag.close()

	time = np.array(sec)+np.array(nsec)*1E-9
	rel_pn = np.array(RP_N)+np.array(N_hp)*1E-3
	rel_pe = np.array(RP_E)+np.array(E_hp)*1E-3
	rel_pd = np.array(RP_D)+np.array(D_hp)*1E-3

	title1 = 'rel_pos'
	title2 = 'flags'

	plot_position_2d([rel_pn,rel_pe], title1)
	plt.figure(2)
	plt.plot(time, flag, label=title2)
	plt.legend('upper left')

def odom_flag_plotter(data, bag):
	sec, nsec, RP_N, RP_E, RP_D, N_hp, E_hp, D_hp, flag = data.get_RelPos(bag)
	odom = data.get_odom(bag)
	bag.close()

	binary_flags = []

	for flg in flag:
		if flg == 311:
			binary_flags.append(1)
		else:
			binary_flags.append(0)

	fig, axs = plt.subplots(4)
	fig.suptitle('odom/flags')
	axs[0].plot(odom.sec, odom.position[0], label = "pn")
	axs[1].plot(odom.sec, odom.position[1], label="pe")
	axs[2].plot(odom.sec, odom.position[2], label="pd")
	axs[3].plot(sec, binary_flags, label="1: fixed ambiguities")
	
def odom_2d_plotter(data, bag, plotname):
	odom = data.get_odom(bag)
	hlc = data.get_high_level_command(bag)
	bag.close()

	label1 = plotname + ' odom'
	label2 = 'hlc'

	plot_position_2d_w_hlc([odom.position[0],odom.position[1]],[hlc.position[0],hlc.position[1]], label1, label2)

def accuracy_plotter(data,bag):
	acc = data.get_PosVelECEF(bag)
	bag.close()

	title = 'accuracy'

	name = ['horizontal_accuracy', 'verticle_accuracy', 'speed_accuracy']
	plot_accuracy(acc, name, title)

def sim_error_plotter(data, bag):
	error = data.get_multirotor_error(bag)
	bag.close()

	title = 'Waypoint error'

	plot_position_1(error, 'error', title)

def plot_position_1(p1, p1_name):

	# fig = plt.plot()
	# fig.title(title)

	plt.plot(p1[0], label = p1_name + " x")
	plt.plot(p1[1], label = p1_name + " y")
	plt.plot(p1[2], label = p1_name + " z")
	plt.legend(loc = "upper right")

def plot_position_2d(p, title):

	plt.figure(1)
	plt.plot(p[0], p[1], label = title)
	plt.legend(loc = "upper left")

def plot_position_2d_w_hlc(p, hlc, label1, label2):

	plt.figure(1)
	plt.plot(p[0], p[1], label = label1)
	plt.plot(hlc[0],hlc[1], label = label2)
	plt.legend(loc = "upper left")

def plot_accuracy(acc, name, title):

	time = np.array(acc[0])+np.array(acc[1])*1E-9

	plt.plot(time, acc[2], label =  name[0])
	plt.plot(time, acc[3], label = name[1])
	plt.plot(time, acc[4], label = name[2])
	plt.legend(loc = "upper right")
	
def plot_compare_position_4(p1, p1_name, p2, p2_name, p3, p3_name, p4, p4_name, cut_time, start_time, end_time, title):

	p1_time = np.array(p1.sec)+np.array(p1.nsec)*1E-9
	p2_time = np.array(p2.sec)+np.array(p2.nsec)*1E-9
	p3_time = np.array(p3.sec)+np.array(p3.nsec)*1E-9
	p4_time = np.array(p4.sec)+np.array(p4.nsec)*1E-9


	if cut_time:
		[start_index, end_index, p1_time] = time_window(p1_time, start_time, end_time)
		x1 = p1.position[0][start_index:end_index]
		y1 = p1.position[1][start_index:end_index]
		z1 = p1.position[2][start_index:end_index]
		[start_index, end_index, p2_time] = time_window(p2_time, start_time, end_time)
		x2 = p2.position[0][start_index:end_index]
		y2 = p2.position[1][start_index:end_index]
		z2 = p2.position[2][start_index:end_index]
		[start_index, end_index, p3_time] = time_window(p3_time, start_time, end_time)
		x3 = p3.position[2][start_index:end_index]
		y3 = p3.position[1][start_index:end_index]
		z3 = p3.position[2][start_index:end_index]
		[start_index, end_index, p4_time] = time_window(p4_time, start_time, end_time)
		x4 = p4.position[0][start_index:end_index]
		y4 = p4.position[1][start_index:end_index]
		z4 = p4.position[2][start_index:end_index]
		#TODO add for the other positions and test.  Change variable names being ploted.
	else:
		x1 = p1.position[0]
		y1 = p1.position[1]
		z1 = p1.position[2]
		x2 = p2.position[0]
		y2 = p2.position[1]
		z2 = p2.position[2]
		x3 = p3.position[0]
		y3 = p3.position[1]
		z3 = p3.position[2]
		x4 = p4.position[0]
		y4 = p4.position[1]
		z4 = p4.position[2]

	fig1, sub = plt.subplots(3)
	fig1.suptitle(title)

	#compare x
	sub[0].plot(p1_time, x1, label = p1_name + " x")
	sub[0].plot(p2_time, x2, label = p2_name + " x")
	sub[0].plot(p3_time, x3, label = p3_name + " x")
	sub[0].plot(p4_time, x4, label = p4_name + " x")
	sub[0].legend(loc = "upper right")
	sub[0].set_xlabel('t [s]')
	sub[0].set_ylabel('x pos')

	#compare y
	sub[1].plot(p1_time, y1, label = p1_name + " y")
	sub[1].plot(p2_time, y2, label = p2_name + " y")
	sub[1].plot(p3_time, y3, label = p3_name + " y")
	sub[1].plot(p4_time, y4, label = p4_name + " y")
	sub[1].legend(loc = "upper right")
	sub[1].set_xlabel('t [s]')
	sub[1].set_ylabel('y pos')
	
	#compare z
	sub[2].plot(p1_time, z1, label = p1_name + " z")
	sub[2].plot(p2_time, z2, label = p2_name + " z")
	sub[2].plot(p3_time, z3, label = p3_name + " z")
	sub[2].plot(p4_time, z4, label = p4_name + " z")
	sub[2].legend(loc = "upper right")
	sub[2].set_xlabel('t [s]')
	sub[2].set_ylabel('z pos')

def plot_compare_position(truth_name, truth, ideal_name, ideal):

	truth_time = np.array(truth.sec)+np.array(truth.nsec)*1E-9
	ideal_time = np.array(ideal.sec)+np.array(ideal.nsec)*1E-9

	fig1, sub = plt.subplots(3)
	fig1.suptitle(truth_name + " vs. " + ideal_name)
	#compare x truth to x ideal
	sub[0].plot(truth_time, truth.position[0], label = truth_name + " x")
	sub[0].plot(ideal_time, ideal.position[0], label = ideal_name + " x")
	sub[0].legend(loc = "upper right")
	sub[0].set_xlabel('t [s]')
	sub[0].set_ylabel('x pos')

	#compare y truth to y ideal
	sub[1].plot(truth_time, truth.position[1], label = truth_name + " y")
	sub[1].plot(ideal_time, ideal.position[1], label = ideal_name + " y")
	sub[1].legend(loc = "upper right")
	sub[1].set_xlabel('t [s]')
	sub[1].set_ylabel('y pos')
	
	#compare z truth to z ideal
	sub[2].plot(truth_time, truth.position[2], label = truth_name + " z")
	sub[2].plot(ideal_time, ideal.position[2], label = ideal_name + " z")
	sub[2].legend(loc = "upper right")
	sub[2].set_xlabel('t [s]')
	sub[2].set_ylabel('z pos')

def plot_bool(bool_name, boolean):

	new_bool = []
	for i in range(len(boolean)):
		if boolean == True:
			new_bool.append(1)
		elif boolean == False:
			new_bool.append(0)
		# else:
		# 	print('bad boolean')
	#compare x truth to x ideal
	plt.plot(new_bool)

def time_window(topic_time, start_time, end_time):
	
	start_index = 0
	while topic_time[start_index] < start_time:
		start_index = start_index+1
	end_index = start_index
	while topic_time[end_index] < end_time:
		end_index = end_index+1
	
	time = topic_time[start_index:end_index]
	return(start_index, end_index, time)

if __name__ == '__main__':
	main()
