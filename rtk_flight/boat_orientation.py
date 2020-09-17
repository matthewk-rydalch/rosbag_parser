from rosbag_parser import Parser
import matplotlib.pyplot as plt
from IPython.core.debugger import set_trace
import rosbag
import numpy as np
from collections import namedtuple

def main():
	
	data = Parser()

	filename = 'test_rfh.bag'
	bag = rosbag.Bag('../../data/boatLanding_sim/' + filename)

	truth, imu, odom = get_data(data, bag)
	get_roll_data(truth, imu, odom)
	get_pitch_data(truth, imu, odom)
	get_yaw_data(truth, imu, odom)


def get_data(data, bag):		

	truth = data.get_truth_boat(bag)

	imu = data.get_imu(bag)

	odom = data.get_multirotor_odom(bag)
	
	bag.close()

	return truth, imu, odom


def get_roll_data(truth, imu, odom):

	truth_time = truth.time
	truth_quat = truth.orientation
	truth_euler = quat2euler(truth_quat)
	truth_phi = truth_euler[0]
	
	odom_time = odom.time
	odom_quat = odom.orientation
	odom_euler = quat2euler(odom_quat)
	odom_phi = odom_euler[0]

	imu_time = imu.time
	imu_wx = imu.wx
	imu_phi_int = integrate(imu_wx, imu_time)
	imu_quat = [imu.qw, imu.qx, imu.qy, imu.qz]
	imu_euler = quat2euler(imu_quat)
	imu_phi = imu_euler[0]

	fig_num = 1
	# plot_3(fig_num, truth_time, truth_phi, 'truth', imu_time, imu_phi, 'imu', odom_time, odom_phi, 'odom')
	plot_2(fig_num, imu_time, imu_phi, 'imu phi', odom_time, odom_phi, 'odom phi')
	# plot_1(fig_num, truth_time, truth_phi, 'truth phi')


def get_pitch_data(truth, imu, odom):

	truth_time = truth.time
	truth_quat = truth.orientation
	truth_euler = quat2euler(truth_quat)
	truth_theta = truth_euler[1]
	
	odom_time = odom.time
	odom_quat = odom.orientation
	odom_euler = quat2euler(odom_quat)
	odom_theta = odom_euler[1]

	imu_time = imu.time
	imu_wy = imu.wy
	imu_theta_int = integrate(imu_wy, imu_time)
	imu_quat = [imu.qw, imu.qx, imu.qy, imu.qz]
	imu_euler = quat2euler(imu_quat)
	imu_theta = imu_euler[1]

	fig_num = 2
	# plot_3(fig_num, truth_time, truth_theta, 'truth', imu_time, imu_theta, 'imu', odom_time, odom_theta, 'odom')
	plot_2(fig_num, imu_time, imu_theta, 'imu theta', odom_time, odom_theta, 'odom theta')
	# plot_1(fig_num, truth_time, truth_theta, 'truth theta')


def get_yaw_data(truth, imu, odom):

	truth_time = truth.time
	truth_quat = truth.orientation
	truth_euler = quat2euler(truth_quat)
	truth_psi = truth_euler[2]*180/np.pi
	
	odom_time = odom.time
	odom_quat = odom.orientation
	odom_euler = quat2euler(odom_quat)
	odom_psi = odom_euler[2]

	imu_time = imu.time
	imu_wz = imu.wz
	imu_psi_int = integrate(imu_wz, imu_time)
	imu_quat = [imu.qw, imu.qx, imu.qy, imu.qz]
	imu_euler = quat2euler(imu_quat)
	imu_psi = imu_euler[2]

	fig_num = 3
	# plot_3(fig_num, truth_time, truth_psi, 'truth', imu_time, imu_psi, 'imu', odom_time, odom_psi, 'odom')
	plot_2(fig_num, imu_time, imu_psi, 'imu psi', odom_time, odom_psi, 'odom psi')
	# plot_1(fig_num, truth_time, truth_psi, 'truth psi')


def plot_3(fig_num, t_x, x, xlabel, t_y, y, ylabel, t_z, z, zlabel):

	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.plot(t_z, z, label = zlabel)
	plt.legend(loc = "upper right")

def plot_2(fig_num, t_x, x, xlabel, t_y, y, ylabel):

	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.legend(loc = "upper right")


def plot_1(fig_num, t_x, x, xlabel):

	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.legend(loc = "upper right")


def quat2euler(quat):

	e0 = quat[0]
	e1 = quat[1]
	e2 = quat[2]
	e3 = quat[3]

	phi = []
	theta = []
	psi = []

	for i in range(len(e0)):
		phi.append(np.arctan2(2*(e0[i]*e1[i] + e2[i]*e3[i]), (e0[i]**2 + e3[i]**2 - e1[i]**2 - e2[i]**2)))
		theta.append(np.arcsin(2*(e0[i]*e2[i] - e1[i]*e3[i])))
		psi.append(np.arctan2(2*(e0[i]*e3[i] + e1[i]*e2[i]), (e0[i]**2 + e1[i]**2 - e2[i]**2 - e3[i]**2)))

	return np.array([phi, theta, psi])


def integrate(x_dot, time):

	#left numerical reiman sum integration
	size = len(x_dot)
	x = np.zeros(size)
	i = 0
	for i in range(size-1):
		dt = time[i]-time[i+1]
		x[i+1] = x[i] + x_dot[i]*dt
	
	return x


if __name__ == '__main__':
	main()
