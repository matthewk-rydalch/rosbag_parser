from rosbag_parser3 import Parser
from rosbag_parser3 import PosTime
from IPython.core.debugger import set_trace 
import matplotlib.pyplot as plt
import rosbag
import numpy as np
import statistics as stats
def main():
	baseEstimation = True

	#### No Base Estimation ####
	## flight B 0318 no base estimator
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0318/flightB.bag')
	# timeInterval = [1616083348.0,1616083367.0] #flight b I think these two flight's data got mixed up.
	## flight C 0318 no base estimator
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0318/flightC.bag')
	# timeInterval = [1616083867.0,1616083890.0] #swaped with b?

	#### Standard ####
	## flight A 0424
	bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightA.bag')
	timeInterval = [1619195374.0,1619195396.0]
	## flight B 0424
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightB.bag')
	# timeInterval = [1619195667.0,1619195689.0]
	## flight C 0424
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightC.bag')
	# timeInterval = [1619194301.0,1619194324.0]
	## flight D 0424
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightD.bag')
	# timeInterval = [1619194546.0,1619194559.0]
	## flight E 0424
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightE.bag')
	# timeInterval = [1619194982.0,1619195012.0]
	## flight F 0424
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightF.bag')
	# timeInterval = [1619195262.0,1619195286.0]

	#### Fast ####
	## flight A 0420
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/flightAFast.bag')
	# timeInterval = [1618694678.0,1618694726.0]
	## flight B 0420
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/flightB.bag')
	# timeInterval = [1618695376.0,1618695396.0]
	## flight D 0420
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/flightD.bag')
	# timeInterval = [1618693725.0,1618693769.0]
	## flight E 0420
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/flightE.bag')
	# timeInterval = [1618694123.0,1618694142.0]

	#### Sway ####
	## flight G 0424
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightG.bag')
	# timeInterval = [1619195524.0,1619195554.0]
	## Flight I 0424
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0424/flightI.bag')
	# timeInterval = [1619195917.0,1619195935.0]

	#### Turn ####
	## flight G 0420
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/flightg.bag')
	# timeInterval = [1618694713.0,1618694782.0]
	## flight H 0420
	# bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0420/flightH.bag')
	# timeInterval = [1618695170.0,1618695308.0]


	if baseEstimation:
		roverOdomTopic = '/rover_odom'
		hlcTopic = '/hlc'
		plot_trajectory(bag,timeInterval,roverOdomTopic,hlcTopic)
	else:
		roverOdomTopic = '/estimate'
		hlcTopic = '/hlc'
		plot_trajectory(bag,timeInterval,roverOdomTopic,hlcTopic)
	
def plot_trajectory(bag,timeInterval,roverOdomTopic,hlcTopic):
	data = Parser(roverOdomTopic,hlcTopic)

	posTime = data.get_rover_odom(bag)
	hlcTime = data.get_hlc(bag)
	errorTime = get_error(posTime,hlcTime)

	labelPosX = 'pn'
	labelPosY = 'pe'
	labelPosZ = 'pd'
	labelHlcX = 'pn_c'
	labelHlcY = 'pe_c'
	labelHlcZ = 'pd_c'

	plot2_interval(posTime.time,posTime.position[0],hlcTime.time,hlcTime.position[0],labelPosX,labelHlcX,timeInterval,1)
	plot2_interval(posTime.time,posTime.position[1],hlcTime.time,hlcTime.position[1],labelPosY,labelHlcY,timeInterval,2)
	plot2_interval(posTime.time,posTime.position[2],hlcTime.time,hlcTime.position[2],labelPosZ,labelHlcZ,timeInterval,3)
	plot3_interval(errorTime,timeInterval,4)

	plt.show()


def get_error(posTime,hlcTime):
	errorX = []
	errorY = []
	errorZ = []
	j = 0
	tHlc = hlcTime.time[j]
	for i in range(len(posTime.time)):
		tPos = posTime.time[i]
		while tHlc < tPos:
			if j == len(hlcTime.time)-1:
				break
			j = j+1
			tHlc = hlcTime.time[j]
		errorVectorI = hlcTime.position.T[j] - posTime.position.T[i]
		errorX.append(errorVectorI[0])
		errorY.append(errorVectorI[1])
		errorZ.append(errorVectorI[2])
	errorTime = PosTime(posTime.time, np.zeros(len(posTime.time)),errorX,errorY,errorZ)
	return errorTime
	

def plot2_interval(t,x,tc,xc,labelX,labelXc,timeInterval,figNum):
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
	plt.legend(bbox_to_anchor=(1.2,1))
	plt.tight_layout()

def plot3_interval(posTimeStruct,timeInterval,figNum):
	tInterval = []
	xInterval = []
	yInterval = []
	zInterval = []

	for i in range(len(posTimeStruct.time)):
		if posTimeStruct.time[i] > timeInterval[0] and posTimeStruct.time[i] < timeInterval[1]:
			tInterval.append(posTimeStruct.time[i] - timeInterval[0])
			xInterval.append(posTimeStruct.position[0][i])
			yInterval.append(posTimeStruct.position[1][i])
			zInterval.append(posTimeStruct.position[2][i])

	plt.figure(figNum)
	plt.plot(tInterval,xInterval,label = 'north error')
	plt.plot(tInterval,yInterval,label = 'east error')
	plt.plot(tInterval,zInterval,label = 'down error')
	plt.plot([0.0,timeInterval[1]-timeInterval[0]],[0.0,0.0],label = 'zero')
	plt.legend(bbox_to_anchor=(1.05,1))
	plt.tight_layout()

if __name__ == '__main__':
	main()
