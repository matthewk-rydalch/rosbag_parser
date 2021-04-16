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
	data = Parser(flightModeTopic,missionStateTopic,baseGpsTopic,baseImuTopic,roverRelPosTopic)
	filename = 'p2u.bag'
	bag = rosbag.Bag('/home/matt/data/boatLanding_sim/' + filename)

	flightMode,missionState,gps,imu,relPos = get_data(data,bag)

	timeOfFlight,timeInterval = calc_time_of_flight(flightMode,missionState)
	speedTimeIndeces = find_time_interval_indeces(gps,timeInterval)
	speedMean,speedStdDev = calc_speed_data(gps,speedTimeIndeces)
	accelTimeIndeces = find_time_interval_indeces(imu,timeInterval)
	accelMean,accelStdDev = calc_accel_data(imu,accelTimeIndeces)
	angRatesTimeIndeces = find_time_interval_indeces(imu,timeInterval)
	angRatesMean,angRatesStdDev = calc_ang_rates_data(imu,angRatesTimeIndeces)

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
	for mode in flightMode:
		if mode.flightMode == 7:
			startTime = mode.time
			break

	for state in missionState:
		if state.missionState == 3:
			endTime = state.time
			break

	timeOfFlight = endTime - startTime
	timeInterval = [startTime,endTime]
	return timeOfFlight, timeInterval

def find_time_interval_indeces(x,timeInterval):
	startIndex = 0
	endIndex = 0
	for y in x:
		if y.time >= timeInterval[0]:
			break
		else:
			startIndex = startIndex+1
	for z in x:
		if z.time >= timeInterval[1]:
			break
		else:
			endIndex = endIndex+1
	timeIntervalIndeces = [startIndex,endIndex]
	return timeIntervalIndeces

def calc_speed_data(gps,timeIndeces):
	speedList = []
	for i in range(timeIndeces):
		normVelocityI = np.linalg.norm(gps.velocity)
		speedList.append(normVelocityI)
	speedMean = stats.mean(speedList)
	speedStdDev = stats.stdev(speedList)
	return speedMean,speedStdDev

def calc_accel_data(imu,timeIndeces):
	accelList = []
	for i in range(timeIndeces):
		normAccelI = np.linalg.norm(imu.accel)
		accelList.append(normAccelI)
	accelMean = stats.mean(accelList)
	accelStdDev = stats.stdev(accelList)
	return accelMean,accelStdDev

def calc_ang_rates_data(imu,timeIndeces):
	omegaList = []
	for i in range(timeIndeces):
		normOmegaI = np.linalg.norm(imu.omega)
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
