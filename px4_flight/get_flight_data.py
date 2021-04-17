from rosbag_parser import Parser
from IPython.core.debugger import set_trace 
import matplotlib.pyplot as plt
import rosbag
import numpy as np
import statistics as stats
def main():
	flightModeTopic = '/flight_mode'
	missionStateTopic = '/mission_state'
	baseGpsTopic = '/p2u/base/PosVelEcef'
	baseImuTopic = '/base/imu'
	roverRelPosTopic = '/p2u/rover/RelPos'
	data = Parser(flightModeTopic,missionStateTopic,baseGpsTopic,baseImuTopic,roverRelPosTopic)
	filename = 'p2u.bag'
	bag = rosbag.Bag('/home/matt/data/boatLanding_sim/' + filename)

	flightMode,missionState,gps,imu,relPos = get_data(data,bag)

	timeOfFlight,timeInterval = calc_time_of_flight(flightMode,missionState)
	relPosTimeIndeces = find_time_interval_indeces(relPos,timeInterval)
	relPosStart = calc_rel_pos_start_data(relPos,relPosTimeIndeces)
	speedTimeIndeces = find_time_interval_indeces(gps,timeInterval)
	speedMean,speedStdDev = calc_speed_data(gps,speedTimeIndeces)
	accelTimeIndeces = find_time_interval_indeces(imu,timeInterval)
	accelMean,accelStdDev = calc_accel_data(imu,accelTimeIndeces)
	angRatesTimeIndeces = find_time_interval_indeces(imu,timeInterval)
	angRatesMean,angRatesStdDev = calc_ang_rates_data(imu,angRatesTimeIndeces)

	print('starting distance away', relPosStart)
	
	print('time of flight = ', timeOfFlight)

	print('speed data:')
	print('		mean = ', speedMean)
	print('		std dev = ', speedStdDev)

	print('accel data:')
	print('		mean = ', accelMean)
	print('		std dev = ', accelStdDev)

	print('angular rates data:')
	print('		mean = ', angRatesMean)
	print('		std dev = ', angRatesStdDev)

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

def calc_rel_pos_start_data(relPos,timeIndeces):
	relPosStart = np.linalg.norm(relPos.position[:,timeIndeces[0]])
	return relPosStart

def calc_speed_data(gps,timeIndeces):
	speedList = []
	for i in range(timeIndeces[0],timeIndeces[1]):
		normVelocityI = np.linalg.norm(gps.velocity[:,i])
		speedList.append(normVelocityI)
	speedMean = stats.mean(speedList)
	speedStdDev = stats.stdev(speedList)
	return speedMean,speedStdDev

def calc_accel_data(imu,timeIndeces):
	accelList = []
	for i in range(timeIndeces[0],timeIndeces[1]):
		normAccelI = np.linalg.norm(imu.accel[:,i]) - 9.81
		accelList.append(normAccelI)
	accelMean = stats.mean(accelList)
	accelStdDev = stats.stdev(accelList)
	return accelMean,accelStdDev

def calc_ang_rates_data(imu,timeIndeces):
	omegaList = []
	for i in range(timeIndeces[0],timeIndeces[1]):
		normOmegaI = np.linalg.norm(imu.omega[:,i])
		omegaList.append(normOmegaI)
	omegaMean = stats.mean(omegaList)
	omegaStdDev = stats.stdev(omegaList)
	return omegaMean,omegaStdDev

def get_data(data, bag):
	flightMode = data.get_flight_mode(bag)
	missionState = data.get_mission_state(bag)
	gps = data.get_base_gps(bag)
	imu = data.get_imu(bag)
	relPos = data.get_rover_relPos(bag)

	return flightMode,missionState,gps,imu,relPos

if __name__ == '__main__':
	main()
