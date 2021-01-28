from rosbag_parser import Parser
import matplotlib.pyplot as plt
# from IPython.core.debugger import set_trace
import rosbag
import numpy as np
from collections import namedtuple

def main():
	
	data = Parser()

	filename = 'estimated_filtered_alt_error.bag'
	bag = rosbag.Bag('../../data/' + filename)

	# filename = 'alt_error.bag'
	# bag = rosbag.Bag('../../data/ragnarok_tests/flights_0125/' + filename)

	odom, roverPVE, boatOdom, boatPVE = get_data(data, bag)
	boatNED = pve2ned(boatPVE, roverPVE)
	roverNED = pve2ned(roverPVE, roverPVE)
	get_north_data(odom, roverNED, boatOdom, boatNED)
	get_east_data(odom, roverNED, boatOdom, boatNED)
	get_down_data(odom, roverNED, boatOdom, boatNED)

def pve2ned(pve, originSet):
	ned = pve
	length = len(pve.time)
	position = np.array(pve.position).T
	origin = np.array(originSet.position).T[0]
	lla = np.array(originSet.lla).T[0]
	for i in range(length):
		positionNED = ecef2ned(position[i], origin, lla)
		ned.position[0][i] = positionNED[0]
		ned.position[1][i] = positionNED[1]
		ned.position[2][i] = positionNED[2]
	return ned

def ecef2ned(ecef, ecefOrigin, refLla):

	lon = refLla[1]*np.pi/180.0
	lat = refLla[0]*np.pi/180.0
	Clon = np.cos(lon)
	Slon = np.sin(lon)
	Clat = np.cos(-lat) #because ublox reports it positive when it should be negative
	Slat = np.sin(-lat)
	C90 = np.cos(-np.pi/2.0)
	S90 = np.sin(-np.pi/2.0)

	Hecef = np.array([[1.0, 0.0, 0.0, ecef[0]],
				   [0.0, 1.0, 0.0, ecef[1]],
				   [0.0, 0.0, 1.0, ecef[2]],
				   [0.0, 0.0, 0.0, 1.0]])

	Ht = np.array([[1.0, 0.0, 0.0, -ecefOrigin[0]],
				   [0.0, 1.0, 0.0, -ecefOrigin[1]],
				   [0.0, 0.0, 1.0, -ecefOrigin[2]],
				   [0.0, 0.0, 0.0, 1.0]])

	Hz = np.array([[Clon, Slon, 0.0, 0.0],
				   [-Slon, Clon, 0.0, 0.0],
				   [0.0, 0.0, 1.0, 0.0],
				   [0.0, 0.0, 0.0, 1.0]])

	Hy =  np.array([[Clat, 0.0, -Slat, 0.0],
				   [0.0, 1.0, 0.0, 0.0],
				   [Slat, 0.0, Clat, 0.0],
				   [0.0, 0.0, 0.0, 1.0]])

	H90 = np.array([[C90, 0.0, -S90, 0.0],
				   [0.0, 1.0, 0.0, 0.0],
				   [S90, 0.0, C90, 0.0],
				   [0.0, 0.0, 0.0, 1.0]])

	Hned = H90@Hy@Hz@Ht@Hecef
	ned = np.array([Hned[0][3], Hned[1][3], Hned[2][3]])

	return ned

def get_data(data, bag):

	odom = data.get_odom(bag)
	roverEcef = data.get_PosVelECEF(bag)
	boatOdom = data.get_boat_odom(bag)
	boatEcef = data.get_boat_PosVelECEF(bag)
	bag.close()

	return odom, roverEcef, boatOdom, boatEcef


def get_north_data(odom, roverNED, boatOdom, boatNED):

	odom_time = odom.time - odom.time[0] - 9.27
	odom_n = np.array(odom.position[0])
	rover_time = roverNED.time - roverNED.time[0]
	boatOdom_time = boatOdom.time - boatOdom.time[0]+9.3
	boatOdom_n = np.array(boatOdom.position[0])
	boat_time = boatNED.time - boatNED.time[0]
	fig_num = 1
	plot_2(fig_num, rover_time, roverNED.position[0],'rover gps north', odom_time, odom_n, 'rover odom north')
	fig_num = 2
	plot_2(fig_num, boat_time, boatNED.position[0], 'boat gps north', boatOdom_time, boatOdom_n, 'boat odom north')


def get_east_data(odom, roverNED, boatOdom, boatNED):

	odom_time = odom.time - odom.time[0] - 9.27
	odom_e = np.array(odom.position[1])
	rover_time = roverNED.time - roverNED.time[0]
	boatOdom_time = boatOdom.time - boatOdom.time[0]+9.3
	boatOdom_e = np.array(boatOdom.position[1])
	boat_time = boatNED.time - boatNED.time[0]
	fig_num = 3
	plot_2(fig_num, rover_time, roverNED.position[1],'rover gps east', odom_time, odom_e, 'rover odom east')
	fig_num = 4
	plot_2(fig_num, boat_time, boatNED.position[1], 'boat gps east', boatOdom_time, boatOdom_e, 'boat odom east')

def get_down_data(odom, roverNED, boatOdom, boatNED):

	odom_time = odom.time - odom.time[0] - 9.27
	odom_d = np.array(odom.position[2])
	rover_time = roverNED.time - roverNED.time[0]
	boatOdom_time = boatOdom.time - boatOdom.time[0]+9.3
	boatOdom_d = np.array(boatOdom.position[2])
	boat_time = boatNED.time - boatNED.time[0]
	fig_num = 5
	plot_2(fig_num, rover_time, roverNED.position[2],'rover gps down', odom_time, odom_d, 'rover odom down')
	fig_num = 6
	plot_2(fig_num, boat_time, boatNED.position[2], 'boat gps down', boatOdom_time, boatOdom_d, 'boat odom down')

def plot_2(fig_num, t_x, x, xlabel, t_y, y, ylabel):

	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.legend(loc = "upper right")
	plt.show()


if __name__ == '__main__':
	main()
