from rosbag_parser import Parser
import matplotlib.pyplot as plt
from IPython.core.debugger import set_trace
import rosbag
import numpy as np
from collections import namedtuple

def main():
	
	data = Parser()

	filename = 'moving_landing2.bag'
	bag = rosbag.Bag('../../../data/ragnarok_tests/flights_0729/' + filename)

	# data_type = 'm2u'
	data_type = 'outdoor'
	# data_type = 'sim'
	odom, gps, imu = get_data(data, bag, data_type)
	get_north_data(odom, gps, imu)
	get_east_data(odom, gps, imu)
	get_height_data(odom, gps, imu)


def get_data(data, bag, data_type):

	if data_type == 'm2u':
	
		odom = data.get_odom(bag)
	
		gps = data.get_ragnarok_ned(bag) #used for mocap2ublox
	
		imu = data.get_imu(bag)
	
	elif data_type == 'outdoor':
	
		odom = data.get_odom(bag)		

		gps_data = data.get_PosVelECEF(bag)
		lla_data = gps_data[0]
		ecef_data = gps_data[1]
		ecef = np.array([ecef_data.x, ecef_data.y, ecef_data.z])
		lla = np.array([lla_data.lat, lla_data.lon, lla_data.alt])
		ned = ecef2ned(ecef, lla).T
		gps = nedTime(lla_data.time, ned[0], ned[1], ned[2])

		imu = data.get_imu(bag)
	
	elif data_type == 'sim':
	
		odom = data.get_multirotor_odom(bag)

		gps = data.get_multirotor_ned(bag)
		
		imu = data.get_multirotor_imu(bag)
	
	else:
		print('invalid data_type')
	
	bag.close()

	return odom, gps, imu


def get_north_data(odom, gps, imu):

	odom_time = odom.time
	odom_n = np.array(odom.position[0])

	gps_time = gps.time
	gps_n = np.array(gps.n)

	imu_time = imu.time
	imu_n = integrate(imu.n, imu_time)

	fig_num = 1
	plot_3(fig_num, odom_time, odom_n, 'odom', gps_time, gps_n, 'gps', imu_time, imu_n, 'imu')


def get_east_data(odom, gps, imu):

	odom_time = odom.time
	odom_e = np.array(odom.position[1])

	gps_time = gps.time
	gps_e = np.array(gps.e)

	imu_time = imu.time
	imu_e = integrate(imu.e, imu_time)

	fig_num = 2
	plot_3(fig_num, odom_time, odom_e, 'odom', gps_time, gps_e, 'gps', imu_time, imu_e, 'imu')


def get_height_data(odom, gps, imu):

	odom_time = odom.time
	odom_h = -np.array(odom.position[2])

	gps_time = gps.time
	gps_h = -np.array(gps.d)

	gravity = -9.81
	imu_time = imu.time
	imu_d = np.array(imu.d) - gravity
	imu_h = integrate(imu_d, imu_time)

	fig_num = 3
	plot_3(fig_num, odom_time, odom_h, 'odom', gps_time, gps_h, 'gps', imu_time, imu_h, 'imu')


def plot_3(fig_num, t_x, x, xlabel, t_y, y, ylabel, t_z, z, zlabel):

	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.plot(t_z, z, label = zlabel)
	plt.legend(loc = "upper right")


def integrate(x_dot, time):

	#left numerical reiman sum integration
	size = len(x_dot)
	x = np.zeros(size)
	i = 0
	for i in range(size-1):
		dt = time[i]-time[i+1]
		x[i+1] = x[i] + x_dot[i]*dt
	
	return x


def ecef2ned(ecef, lla):

	size = len(ecef.T)
	origin = np.array([ecef[:,0]]).T
	ecef = ecef-origin

	ned = np.zeros((size, 3))
	
	lat = lla[0]
	lon = lla[1]

	#don't know why @ isn't working for matrix multiplication
	# ned = Ry(lat).T@Rx(-lon).T@Ry(90.0).T@ned
	for i in range(size):
		ned[i] = np.matmul(np.matmul(np.matmul(Ry(lat[i]).T,Rx(-lon[i]).T),Ry(90.0).T),ecef[:,i])

	return ned


def Rx(theta):
	
	theta = theta*np.pi/180.0
	st = np.sin(theta)
	ct = np.cos(theta)
	rotx = np.array([[1.0, 0.0, 0.0], \
					[0.0, ct, st], \
					[0.0, -st, ct]])

	return rotx


def Ry(theta):
	
	theta = theta*np.pi/180.0
	st = np.sin(theta)
	ct = np.cos(theta)
	roty = np.array([[ct, 0.0, -st], \
					[0.0, 1.0, 0.0], \
					[st, 0.0, ct]])

	return roty


def Rz(theta):

	theta = theta*np.pi/180.0
	st = np.sin(theta)
	ct = np.cos(theta)
	rotz = np.array([[ct, st, 0.0], \
					[-st, ct, 0.0], \
					[0.0, 0.0, 1.0]])

	return rotz


class nedTime:
	def __init__(self, time, north, east, down):
		
		self.time = time
		
		self.n = north
		self.e = east
		self.d = down


if __name__ == '__main__':
	main()
