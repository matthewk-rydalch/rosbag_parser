from rosbag_parser4 import Parser
from IPython.core.debugger import set_trace 
import matplotlib.pyplot as plt
import matplotlib.axes as ax
import rosbag
import numpy as np
import statistics as stats
def main():
	#### Standard ####
	# ## flight A 0424
	# flightNum = 1
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightA.bag')
	# get_data(bag,flightNum)
	# ## flight B 0424
	# flightNum = 2
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightB.bag')
	# get_data(bag,flightNum)
	## flight C 0424
	# flightNum = 3
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightC.bag')
	# get_data(bag,flightNum)
	# ## flight D 0424
	# flightNum = 4
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightD.bag')
	# get_data(bag,flightNum)
	# ## flight E 0424
	# flightNum = 5
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightE.bag')
	# get_data(bag,flightNum)
	# ## flight F 0424
	# flightNum = 6
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightF.bag')
	# get_data(bag,flightNum)

	# #### Fast ####
	## flight A 0420
	flightNum = 7
	bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/flightAFast.bag')
	get_data(bag,flightNum)
	## flight B 0420
	flightNum = 8
	bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/flightB.bag')
	get_data(bag,flightNum)
	## flight D 0420
	flightNum = 9
	bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/flightD.bag')
	get_data(bag,flightNum)
	## flight E 0420
	flightNum = 10
	bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/flightE.bag')
	get_data(bag,flightNum)

	# #### Sway ####
	# ## flight G 0424
	# flightNum = 11
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightG.bag')
	# get_data(bag,flightNum)
	# ## Flight I 0424
	# flightNum = 12
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightI.bag')
	# get_data(bag,flightNum)

	# #### Turn ####
	# ## flight G 0420
	# flightNum = 13
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/flightg.bag')
	# get_data(bag,flightNum)
	# ## flight H 0420
	# flightNum = 14
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/flightH.bag')
	# get_data(bag,flightNum)

	plt.show()

def get_data(bag,flightNum):
	roverOdomTopic = '/rover_odom'
	hlcTopic = '/hlc'
	boatOdomTopic = '/base_odom'
	missionStateTopic = '/mission_state'
	flightModeTopic = '/flight_mode'
	data = Parser(roverOdomTopic,hlcTopic,boatOdomTopic,missionStateTopic,flightModeTopic)

	posTime = data.get_rover_odom(bag)
	hlcTime = data.get_hlc(bag)
	errorTime = data.get_boat_odom(bag)
	stateTime = data.get_mission_state(bag)
	modeTime = data.get_flight_mode(bag)

	timeInterval = get_time_interval(stateTime,modeTime)

	print('FLIGHT: ', flightNum)
	labelPosX = 'pn'
	labelPosY = 'pe'
	labelPosZ = 'pd'
	labelHlcX = 'pn_c'
	labelHlcY = 'pe_c'
	labelHlcZ = 'pd_c'
	tTouchDown = plot3_interval(errorTime,timeInterval,flightNum*2+3)
	plot2_interval(posTime.time,posTime.position[0],hlcTime.time,hlcTime.position[0],labelPosX,labelHlcX,timeInterval,tTouchDown,flightNum)
	plot2_interval(posTime.time,posTime.position[1],hlcTime.time,hlcTime.position[1],labelPosY,labelHlcY,timeInterval,tTouchDown,flightNum+1)
	plot2_interval(posTime.time,posTime.position[2],hlcTime.time,hlcTime.position[2],labelPosZ,labelHlcZ,timeInterval,tTouchDown,flightNum+2)

def get_time_interval(stateTimeStruct,modeTimeStruct):
	timeInterval = []
	for i in range(len(modeTimeStruct.time)):
		if modeTimeStruct.val[i] == 7.0:
			timeInterval.append(modeTimeStruct.time[i])
			break
	for i in range(len(stateTimeStruct.time)):
		if stateTimeStruct.val[i] == 3.0:
			timeInterval.append(stateTimeStruct.time[i]+3.0)
			break
	return timeInterval

def plot2_interval(t,x,tc,xc,labelX,labelXc,timeInterval,tTouchDown,figNum):
	tInterval = []
	xInterval = []
	tcInterval = []
	xcInterval = []

	for i in range(len(t)):
		if t[i] > timeInterval[0] and t[i] < timeInterval[1]:
			tInterval.append(t[i] - timeInterval[0])
			xInterval.append(x[i])
	for j in range(len(tc)):
		if tc[j] > timeInterval[0] and tc[j] < timeInterval[1]:
			tcInterval.append(tc[j] - timeInterval[0])
			xcInterval.append(xc[j])
	plt.figure(figNum)
	plt.plot(tInterval,xInterval,label = labelX)
	plt.plot(tcInterval,xcInterval,label = labelXc)
	# ax.Axes.axvline(plt,tTouchDown)
	plt.axvline(tTouchDown,label='touch down',color='gray',dashes=(2,1))
	plt.legend(bbox_to_anchor=(1.35,1))
	plt.tight_layout()

def plot3_interval(posTimeStruct,timeInterval,figNum):

	tInterval = []
	xInterval = []
	yInterval = []
	zInterval = []
	zPositive = False

	for i in range(len(posTimeStruct.time)):
		if posTimeStruct.time[i] > timeInterval[0] and posTimeStruct.time[i] < timeInterval[1]:
			tInterval.append(posTimeStruct.time[i] - timeInterval[0])
			xInterval.append(posTimeStruct.position[0][i])
			yInterval.append(posTimeStruct.position[1][i])
			zInterval.append(posTimeStruct.position[2][i])
			if zInterval[-1] > 0.0:
				zPositive = True
			if zPositive == True and zInterval[-1] < 0.0:
				tTouchDown = tInterval[-1]
				xTouchDown = xInterval[-1]
				yTouchDown = yInterval[-1]
				eTouchDown = np.linalg.norm([xTouchDown,yTouchDown])
				print('time of flight =', tTouchDown)
				print('north error = ', xTouchDown)
				print('east error = ', yTouchDown)
				print('total error = ', eTouchDown)

				zPositive = False

	plt.figure(figNum)
	plt.plot(tInterval,xInterval,label = 'error n')
	plt.plot(tInterval,yInterval,label = 'error e')
	plt.plot(tInterval,zInterval,label = 'error d')
	plt.axhline(0.0,label='zero',color='black',dashes=(2,1))
	plt.axvline(tTouchDown,label='touch down',color='gray',dashes=(2,1))
	plt.legend(bbox_to_anchor=(1.35,1))
	plt.tight_layout()
	return tTouchDown

if __name__ == '__main__':
	main()
