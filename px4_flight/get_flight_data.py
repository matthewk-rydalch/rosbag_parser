from rosbag_parser import Parser
from IPython.core.debugger import set_trace 
import matplotlib.pyplot as plt
import rosbag
import numpy as np
import statistics as stats
def main():
	flightModeTopic = '/flight_mode'
	missionStateTopic = '/mission_state'
	baseGpsTopic = '/base/PosVelEcef'
	baseImuTopic = '/base/imu'
	roverRelPosTopic = '/rover/RelPos'
	roverGpsTopic = '/dummyTopic'
	baseOdomTopic = '/dummyTopic'
	data = Parser(flightModeTopic,missionStateTopic,baseGpsTopic,baseImuTopic,roverRelPosTopic,roverGpsTopic,baseOdomTopic)
	bagNames1 = ['flightAFast.bag','flightB.bag','flightD.bag','flightE.bag','flightg.bag','flightH.bag']
	bagNames2 = ['flightA.bag','flightB.bag','flightC.bag','flightD.bag','flightE.bag','flightF.bag','flightH.bag','flightI.bag']

	timeOfFlightList = []
	startDistanceList = []
	speedList = []
	accelList = []
	angRatesList = []
	for i in range(len(bagNames1)):
		bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/' + bagNames1[i])
		flightMode,missionState,gps,imu,relPos = get_data(data,bag)

		timeOfFlight,timeInterval = calc_time_of_flight(flightMode,missionState)
		timeOfFlightList.append(timeOfFlight)
		print('time of flight = ', timeOfFlight)
		relPosTimeIndeces = find_time_interval_indeces(relPos,timeInterval)
		startDistance = calc_start_distance_data(relPos,relPosTimeIndeces)
		startDistanceList.append(startDistance)

		speedTimeIndeces = find_time_interval_indeces(gps,timeInterval)
		speed = calc_speed_data(gps,speedTimeIndeces)
		speedList.extend(speed)

		accelTimeIndeces = find_time_interval_indeces(imu,timeInterval)
		accel = calc_accel_data(imu,accelTimeIndeces)
		accelList.extend(accel)

		angRatesTimeIndeces = find_time_interval_indeces(imu,timeInterval)
		angRates = calc_ang_rates_data(imu,angRatesTimeIndeces)
		angRatesList.extend(angRates)

	for j in range(len(bagNames2)):
		bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/' + bagNames2[j])
		flightMode,missionState,gps,imu,relPos = get_data(data,bag)

		timeOfFlight,timeInterval = calc_time_of_flight(flightMode,missionState)
		timeOfFlightList.append(timeOfFlight)
		print('time of flight = ', timeOfFlight)
		relPosTimeIndeces = find_time_interval_indeces(relPos,timeInterval)
		startDistance = calc_start_distance_data(relPos,relPosTimeIndeces)
		startDistanceList.append(startDistance)

		speedTimeIndeces = find_time_interval_indeces(gps,timeInterval)
		speed = calc_speed_data(gps,speedTimeIndeces)
		speedList.extend(speed)

		accelTimeIndeces = find_time_interval_indeces(imu,timeInterval)
		accel = calc_accel_data(imu,accelTimeIndeces)
		accelList.extend(accel)

		angRatesTimeIndeces = find_time_interval_indeces(imu,timeInterval)
		angRates = calc_ang_rates_data(imu,angRatesTimeIndeces)
		angRatesList.extend(angRates)

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

def calc_speed_data(gps,timeIndeces):
	speedList = []
	for i in range(timeIndeces[0],timeIndeces[1]):
		normVelocityI = np.linalg.norm(gps.velocity[:,i])
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
	gps = data.get_base_gps(bag)
	imu = data.get_imu(bag)
	relPos = data.get_rover_relPos(bag)

	return flightMode,missionState,gps,imu,relPos

if __name__ == '__main__':
	main()
