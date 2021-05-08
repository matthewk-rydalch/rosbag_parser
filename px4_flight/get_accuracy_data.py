from rosbag_parser2 import Parser
from IPython.core.debugger import set_trace 
import matplotlib.pyplot as plt
import rosbag
import numpy as np
import statistics as stats
def main():
	roverOdomTopic = '/estimate'
	hlcTopic = '/hlc'
	timeInterval = [1616083372.0,1616083388.0] #flight b I think these two flight's data got mixed up.
	# timeInterval = [1616083890.5,1616083891.5] #flight c b should be c and c should be b
	data = Parser(roverOdomTopic,hlcTopic)
	bag = rosbag.Bag('/home/matt/data/px4flight/outdoor/0318/flightB.bag')

	roverOdom = data.get_rover_odom(bag)
	hlc = data.get_hlc(bag)

	roverPos = get_over_time_interval(roverOdom,timeInterval)
	hlcPos = get_over_time_interval(hlc,timeInterval)

	error = compare_data(roverPos,hlcPos)

	print('error = ', error)

	plt.figure(1)
	plt.plot(roverOdom.time,roverOdom.position[0],label = 'odom x')
	plt.plot(hlc.time,hlc.position[0],label = 'hlc x')
	plt.legend(loc = "upper right")
	plt.figure(2)
	plt.plot(roverOdom.time,roverOdom.position[1],label = 'odom y')
	plt.plot(hlc.time,hlc.position[1],label = 'hlc y')
	plt.legend(loc = "upper right")
	plt.show()

def get_over_time_interval(x,timeInterval):
	i = 0
	xList = []
	timeList = []
	while x.time[i] < timeInterval[0]:
		i = i+1
	while x.time[i] < timeInterval[1]:
		xList.append(x.position.T[i])
		i = i+1
	xArray = np.array(xList)
	return xArray

def compare_data(roverPos,hlcPos):
	roverAveragePosX = stats.mean(roverPos.T[0])
	roverAveragePosY = stats.mean(roverPos.T[1])
	hlcAveragePosX = stats.mean(hlcPos.T[0])
	hlcAveragePosY = stats.mean(hlcPos.T[1])

	errorX = roverAveragePosX - hlcAveragePosX
	errorY = roverAveragePosY - hlcAveragePosY
	error = np.linalg.norm([errorX,errorY])

	return error

if __name__ == '__main__':
	main()
