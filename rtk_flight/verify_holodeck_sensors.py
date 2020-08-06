from rosbag_parser import Parser
import matplotlib.pyplot as plt
from IPython.core.debugger import set_trace
import rosbag
import numpy as np
from collections import namedtuple

def main():
	
	data = Parser()

	filename = 'test_sensors.bag'
	bag = rosbag.Bag('../../data/boatLanding_sim/' + filename)

	odom, imu = get_data(data, bag)
	get_north_data(odom, imu)
	get_east_data(odom, imu)
	get_height_data(odom, imu)


def get_data(data, bag):

	odom = data.get_truth_boat(bag)

	imu = data.get_boatIMU_data(bag)	
	
	bag.close()

	return odom, imu


def get_north_data(odom, imu):

	odom_time = odom.time
	odom_n = np.array(odom.position[0])

	vel_time = odom.time
	vel_n = np.array(odom.velocity[0])
	vel_n = integrate(vel_n, vel_time)

	imu_time = imu.time
	imu_n = integrate(imu.n, imu_time)
	imu_n = integrate(imu_n, imu_time)

	fig_num = 1
	plot_3(fig_num, odom_time, odom_n, 'odom', vel_time, vel_n, 'vel', imu_time, imu_n, 'imu')


def get_east_data(odom, imu):

	odom_time = odom.time
	odom_e = np.array(odom.position[1])

	vel_time = odom.time
	vel_e = np.array(odom.velocity[1])
	vel_e = integrate(vel_e, vel_time)

	imu_time = imu.time
	imu_e = integrate(imu.e, imu_time)
	imu_e = integrate(imu_e, imu_time)

	fig_num = 2
	plot_3(fig_num, odom_time, odom_e, 'odom', vel_time, vel_e, 'vel', imu_time, imu_e, 'imu')


def get_height_data(odom, imu):

	odom_time = odom.time
	odom_h = -np.array(odom.position[2])

	vel_time = odom.time
	vel_d = np.array(odom.velocity[1])
	vel_d = integrate(vel_d, vel_time)

	gravity = -9.81
	imu_time = imu.time
	imu_d = np.array(imu.d) - gravity
	imu_h = integrate(imu_d, imu_time)
	imu_h = integrate(imu_h, imu_time)

	fig_num = 3
	plot_3(fig_num, odom_time, odom_h, 'odom', vel_time, vel_d, 'vel', imu_time, imu_h, 'imu')


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
