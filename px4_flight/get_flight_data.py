from rosbag_parser import Parser
from IPython.core.debugger import set_trace 
import matplotlib.pyplot as plt
import rosbag
import numpy as np
import navpy

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


	 

def get_data(data, bag):
	flightMode = data.get_flight_mode(bag)
	missionState = data.get_mission_state(bag)
	gps = data.get_base_gps(bag)
	imu = data.get_imu(bag)
	relPos = data.get_rover_relPos(bag)

	return flightMode,missionState,gps,imu,relPos

if __name__ == '__main__':
	main()
