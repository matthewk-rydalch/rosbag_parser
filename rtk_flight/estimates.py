from rosbag_parser import Parser
import matplotlib.pyplot as plt
# from IPython.core.debugger import set_trace
import rosbag
import numpy as np
from collections import namedtuple

def main():
	
	data = Parser()

	filename = 'landing_ublox_jan18_5.bag'
	bag = rosbag.Bag('../../data/outdoor/' + filename)

	data_type = 'outdoor'
	# data_type = 'mocap'
	# data_type = 'm2u'
	# data_type = 'outdoor'
	# data_type = 'sim'
	odom, boatOdom, relpos = get_data(data, bag, data_type)
	get_north_data(odom, boatOdom, relpos)
	get_east_data(odom, boatOdom, relpos)
	get_down_data(odom, boatOdom, relpos)




def get_data(data, bag, data_type):

	if data_type == 'outdoor':
		
		odom = data.get_odom(bag)
		boatOdom = data.get_boat_odom(bag)
		relpos = data.get_RelPos(bag)

	else:
		print('invalid data_type')

		bag.close()

	return odom, boatOdom, relpos


def get_north_data(odom, boatOdom, relpos):

	delta_time = []
	delta_n = []
	odom_time = odom.time - odom.time[0]
	odom_n = np.array(odom.position[0])
	boatOdom_time = boatOdom.time - boatOdom.time[0]
	boatOdom_n = np.array(boatOdom.position[0])
	j = 0
	for i in range(len(boatOdom_time)-1):
		while (odom_time[j] < boatOdom_time[i]):
			j = j+1
		delta_time.append(odom_time[j])
		delta_n.append(odom_n[j] - boatOdom_n[i])

	relpos_time = np.array(relpos[0])+np.array(relpos[1])*1E-9
	relpos_time = relpos_time - relpos_time[0]
	relpos_n = np.array(relpos[2])

	fig_num = 1
	plot_2(fig_num, delta_time, delta_n, 'delta', relpos_time, relpos_n, 'relpos')


def get_east_data(odom, boatOdom, relpos):

	delta_time = []
	delta_e = []
	odom_time = odom.time - odom.time[0]
	odom_e = np.array(odom.position[1])
	boatOdom_time = boatOdom.time - boatOdom.time[0]
	boatOdom_e = np.array(boatOdom.position[1])
	j = 0
	for i in range(len(boatOdom_time)-1):
		while (odom_time[j] < boatOdom_time[i]):
			j = j+1
		delta_time.append(odom_time[j])
		delta_e.append(odom_e[j] - boatOdom_e[i])

	relpos_time = np.array(relpos[0])+np.array(relpos[1])*1E-9
	relpos_time = relpos_time - relpos_time[0]
	relpos_e = np.array(relpos[3])


	fig_num = 2
	plot_2(fig_num, delta_time, delta_e, 'delta', relpos_time, relpos_e, 'relpos')


def get_down_data(odom, boatOdom, relpos):

	delta_time = []
	delta_d = []
	odom_time = odom.time - odom.time[0]
	odom_d = np.array(odom.position[2])
	boatOdom_time = boatOdom.time - boatOdom.time[0]
	boatOdom_d = np.array(boatOdom.position[2])
	j = 0
	for i in range(len(boatOdom_time)-1):
		while (odom_time[j] < boatOdom_time[i]):
			j = j+1
		delta_time.append(odom_time[j])
		delta_d.append(odom_d[j] - boatOdom_d[i])

	relpos_time = np.array(relpos[0])+np.array(relpos[1])*1E-9
	relpos_time = relpos_time - relpos_time[0]
	relpos_d = np.array(relpos[4])


	fig_num = 3
	plot_2(fig_num, delta_time, delta_d, 'delta', relpos_time, relpos_d, 'relpos')


def plot_2(fig_num, t_x, x, xlabel, t_y, y, ylabel):

	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.legend(loc = "upper right")
	plt.show()


if __name__ == '__main__':
	main()
