from rosbag_parser import Parser
from IPython.core.debugger import set_trace 
import matplotlib.pyplot as plt
import rosbag
import numpy as np
import statistics as stats
def main():
	""" This script gathers the selected data (defined by the nodes below by calling rosbag_parser.py.
	If there are many bag files, statistics of will be gathered from all the bagfiles in a list (i.e. bagNames1, bagNames2). 
	If there is just one bag file to be looked at, the baseOdomTopic, baseGpsTopic, and roverGpsTopic are plotted
	"""
	# Set topics you wish to extract
	flightModeTopic = '/flight_mode'
	missionStateTopic = '/mission_state'
	baseGpsTopic = '/base/PosVelEcef'
	baseImuTopic = '/base/imu'
	roverRelPosTopic = '/rover/RelPos'
	roverGpsTopic = '/rover/PosVelEcef'
	baseOdomTopic = '/base_odom'
	baseEulerTopic = '/base_euler'
	data = Parser(flightModeTopic,missionStateTopic,baseGpsTopic,baseImuTopic,roverRelPosTopic,roverGpsTopic,baseOdomTopic, baseEulerTopic)
	
	# If there is only one bag file in the list, stats won't be given. If there is more, stats will be given
	bagNames1 = ['outdoor_w_boat_2021-11-11-16-39-38.bag.active'] #, 'outdoor_w_boat_2021-10-30-16-54-00.bag']
	# bagNames1 = ['flightAFast.bag','flightB.bag','flightD.bag','flightE.bag','flightg.bag','flightH.bag']
	# bagNames2 = ['flightA.bag','flightB.bag','flightC.bag','flightD.bag','flightE.bag','flightF.bag','flightH.bag','flightI.bag']

	timeOfFlightList = []
	startDistanceList = []
	speedList = []
	accelList = []
	angRatesList = []
	for i in range(len(bagNames1)):
		bag = rosbag.Bag('../Outdoor data/' + bagNames1[i])
		flightMode,missionState,baseGps,roverGps,imu,relPos,boatOdom, odom = get_data(data,bag)

		timeOfFlight,timeInterval = calc_time_of_flight(flightMode,missionState)
		timeOfFlightList.append(timeOfFlight)
		print('time of flight = ', timeOfFlight)
		relPosTimeIndeces = find_time_interval_indeces(relPos,timeInterval)
		startDistance = calc_start_distance_data(relPos,relPosTimeIndeces)
		startDistanceList.append(startDistance)

		speedTimeIndeces = find_time_interval_indeces(baseGps,timeInterval)
		speed = calc_speed_data(baseGps,speedTimeIndeces)
		speedList.extend(speed)

		accelTimeIndeces = find_time_interval_indeces(imu,timeInterval)
		accel = calc_accel_data(imu,accelTimeIndeces)
		accelList.extend(accel)

		angRatesTimeIndeces = find_time_interval_indeces(imu,timeInterval)
		angRates = calc_ang_rates_data(imu,angRatesTimeIndeces)
		angRatesList.extend(angRates)

	# for j in range(len(bagNames2)):
	# 	bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/' + bagNames2[j])
	# 	flightMode,missionState,baseGps,roverGpsimu,relPos = get_data(data,bag)

	# 	timeOfFlight,timeInterval = calc_time_of_flight(flightMode,missionState)
	# 	timeOfFlightList.append(timeOfFlight)
	# 	print('time of flight = ', timeOfFlight)
	# 	relPosTimeIndeces = find_time_interval_indeces(relPos,timeInterval)
	# 	startDistance = calc_start_distance_data(relPos,relPosTimeIndeces)
	# 	startDistanceList.append(startDistance)

	# 	speedTimeIndeces = find_time_interval_indeces(baseGps,timeInterval)
	# 	speed = calc_speed_data(baseGps,speedTimeIndeces)
	# 	speedList.extend(speed)

	# 	accelTimeIndeces = find_time_interval_indeces(imu,timeInterval)
	# 	accel = calc_accel_data(imu,accelTimeIndeces)
	# 	accelList.extend(accel)

	# 	angRatesTimeIndeces = find_time_interval_indeces(imu,timeInterval)
	# 	angRates = calc_ang_rates_data(imu,angRatesTimeIndeces)
	# 	angRatesList.extend(angRates)

	#if more than one bag file is being analyzed in a list, gather the statistics
	if len(bagNames1) > 1:
		startDistanceMean,startDistanceStdDev = get_stats(startDistanceList)
		speedMean,speedStdDev = get_stats(speedList)
		accelMean,accelStdDev = get_stats(accelList)
		angRatesMean,angRatesStdDev = get_stats(angRatesList)
		timeOfFlightMean,timeOfFlightStdDev = get_stats(timeOfFlightList)

		print('starting distance away data:')
		print('		mean = ', startDistanceMean)
		print('		std dev = ', startDistanceStdDev)

		print('speed data:')
		print('		mean = ', speedMean)
		print('		std dev = ', speedStdDev)

		print('accel data:')
		print('		mean = ', accelMean)
		print('		std dev = ', accelStdDev)

		print('angular rates data:')
		print('		mean = ', angRatesMean)
		print('		std dev = ', angRatesStdDev)
			
		print('time of flight data:')
		print('		mean =', timeOfFlightMean)
		print('		std dev = ', timeOfFlightStdDev)

	# get and plot data
	fig_num = 1
	fig_num = get_north_data(odom[0], boatOdom, fig_num)
	fig_num = get_east_data(odom[0], boatOdom, fig_num)
	fig_num = get_down_data(odom[0], boatOdom, fig_num)
	fig_num = plot_2(fig_num,roverGps[0].time,roverGps[0].position[0], "N Rover GPS", baseGps.time, baseGps.position[0], "N BaseGPS")
	fig_num = plot_2(fig_num,roverGps[0].time,roverGps[0].position[1], "E Rover GPS", baseGps.time, baseGps.position[1], "E BaseGPS")
	fig_num = plot_2(fig_num,roverGps[0].time,roverGps[0].position[2], "D Rover GPS", baseGps.time, baseGps.position[2], "D BaseGPS")
	plt.show()

def calc_time_of_flight(flightMode,missionState):
	startTime = 0.0
	endTime = 0.0
	for i in range(len(flightMode.time)):
		if flightMode.flightMode[i] == 7:
			startTime = flightMode.time[i]
			break
	for j in range(len(missionState.time)):
		if missionState.missionState[j] == 3:
			endTime = missionState.time[j]
			break

	timeOfFlight = endTime - startTime
	timeInterval = [startTime,endTime]
	return timeOfFlight, timeInterval

def find_time_interval_indeces(x,timeInterval):
	for i in range(len(x.time)):
		if x.time[i] >= timeInterval[0]:
			startIndex = i
			break
	for j in range(i,len(x.time)):
		if x.time[j] >= timeInterval[1]:
			endIndex = j
			break
	timeIntervalIndeces = [startIndex,endIndex]
	return timeIntervalIndeces

def calc_start_distance_data(relPos,timeIndeces):
	relPosStart = np.linalg.norm(relPos.position[:,timeIndeces[0]])
	return relPosStart

def calc_speed_data(baseGps,timeIndeces):
	speedList = []
	for i in range(timeIndeces[0],timeIndeces[1]):
		normVelocityI = np.linalg.norm(baseGps.velocity[:,i])
		speedList.append(normVelocityI)
	return speedList

def calc_accel_data(imu,timeIndeces):
	accelList = []
	alpha = 0.02
	filteredAccelX = low_pass_filter(imu.accel[0,:],alpha)
	filteredAccelY = low_pass_filter(imu.accel[1,:],alpha)
	filteredAccelZ = low_pass_filter(imu.accel[2,:],alpha)
	for i in range(timeIndeces[0],timeIndeces[1]):
		accelINoGravity = [filteredAccelX[i],filteredAccelY[i],filteredAccelZ[i]+9.81]
		normAccelI = np.linalg.norm(accelINoGravity)
		accelList.append(normAccelI)
	return accelList

def calc_ang_rates_data(imu,timeIndeces):
	omegaList = []
	alpha = 0.02
	filteredOmegaX = low_pass_filter(imu.omega[0,:],alpha)
	filteredOmegaY = low_pass_filter(imu.omega[1,:],alpha)
	for i in range(timeIndeces[0],timeIndeces[1]):
		omegaIXY = [filteredOmegaX[i],filteredOmegaY[i]]
		normOmegaI = np.linalg.norm(omegaIXY)
		omegaList.append(normOmegaI)
	return omegaList

def low_pass_filter(signal,alpha):
	filteredSignal = []
	filteredSignal0 = signal[0]*alpha
	filteredSignal.append(filteredSignal0)
	for i in range(1,len(signal)):
		filteredSignalI = signal[i]*alpha + filteredSignal[-1]*(1.0-alpha)
		filteredSignal.append(filteredSignalI)
	return filteredSignal

def get_stats(x):
	mean = stats.mean(x)
	stdDev = stats.stdev(x)
	return mean,stdDev

def get_data(data, bag):
	flightMode = data.get_flight_mode(bag)
	missionState = data.get_mission_state(bag)
	baseGps = data.get_base_gps(bag)
	roverGps = data.get_rover_gps(bag)
	imu = data.get_imu(bag)
	relPos = data.get_rover_relPos(bag)
	boatOdom = data.get_boat_odom(bag)
	odom = data.get_odom(bag)
	

	return flightMode,missionState,baseGps, roverGps, imu,relPos,boatOdom, odom

def get_north_data(odom, boatOdom, fig_num):
	"""Function to plot the north data of the rover and boat

	Inputs:
		odom: data from '/rover_odom'
		boatOdom: data from '/base_odom'
		truth: data from 'rhodey_ned'
		boatTruth: data from '/boat_landing_platform_ned'

	"""
	#odom_n = odom.position[0] - odom.position[0][0]
	boat_n = boatOdom.position[0] - odom.position[0][0]

	#fig_num = plot_1(fig_num, odom.time, odom_n, 'N Rover Odom')
	fig_num = plot_1(fig_num, boatOdom.time, boat_n, 'N Boat Odom')

	return fig_num
	
	
def get_east_data(odom, boatOdom, fig_num):
	"""Function to plot the east data of the rover and boat

	Inputs:
		odom: data from '/rover_odom'
		boatOdom: data from '/base_odom'
		truth: data from 'rhodey_ned'
		boatTruth: data from '/boat_landing_platform_ned'

	"""
	#odom_e = odom.position[1] - odom.position[1][0]
	boat_e = boatOdom.position[1] - odom.position[1][0]

	
	#fig_num = plot_2(fig_num, odom.time, odom_e, 'E Rover Odom', truth.time, truth.e, 'E Rover Truth')
	fig_num = plot_1(fig_num, boatOdom.time, boat_e, 'E Boat Odom')
	
	# plot_1(fig_num, odom.time, odom_e, 'E Rover Odom')
	# plot_1(fig_num, truth.time, truth.e, 'E Rover Truth')

	return fig_num

def get_down_data(odom, boatOdom, fig_num):
	"""Function to plot the down data of the rover and boat

	Inputs:
		odom: data from '/rover_odom'
		boatOdom: data from '/base_odom'
		truth: data from 'rhodey_ned'
		boatTruth: data from '/boat_landing_platform_ned'

	"""
	#odom_d = odom.position[2] - odom.position[2][0]
	boat_d = boatOdom.position[2] - odom.position[2][0]

	
	#fig_num = plot_2(fig_num, odom.time, odom_d, 'D Rover Odom', truth.time, truth.d, 'D Rover Truth')
	fig_num = plot_1(fig_num, boatOdom.time, boat_d, 'D Boat Odom')
	
	# plot_1(fig_num, odom.time, odom_e, 'E Rover Odom')
	# plot_1(fig_num, truth.time, truth.e, 'E Rover Truth')

	return fig_num

def plot_2(fig_num, t_x, x, xlabel, t_y, y, ylabel):
	"""Function to plot 2 quantities
	
	Inputs: 
		fig_num (int): figure number
		t_x (array[float]): array of time stamps associated with x
		x (array[float]): array of first data set to plot
		xlabel (string): string label for first data set
		t_y (array[float]): array of time stamps associated with y
		y (array[float]): array of second data set to plot
		ylabel (string): string label for second data set

		"""
	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.legend(loc = "upper right")
	#plt.show()

	fig_num+=1
	return fig_num

def plot_1(fig_num, t_x, x, xlabel):
	"""Function to plot 1 quantity
	
	Inputs: 
		fig_num (int): figure number
		t_x (array[float]): array of time stamps associated with x
		x (array[float]): array of first data set to plot
		xlabel (string): string label for first data set

		"""
	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.legend(loc = "upper right")
	#plt.show()

	fig_num+=1
	return fig_num

if __name__ == '__main__':
	main()
