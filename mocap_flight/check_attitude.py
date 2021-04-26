from rosbag_parser import Parser
from IPython.core.debugger import set_trace 
import matplotlib.pyplot as plt
import rosbag
import numpy as np
from scipy.spatial.transform import Rotation as R

def main():
	mocapTopic = '/boat_landing_platform_ned'
	baseEulerTopic = '/base_euler'
	data = Parser(mocapTopic,baseEulerTopic)
	filename = 'm2u_w_boat.bag'
	bag = rosbag.Bag('/home/matt/data/mocap/' + filename)

	baseEuler, mocapQuat = get_data(data,bag)

	mocapEuler = quat2euler(mocapQuat)

	compare_roll_data(mocapEuler,baseEuler)
	compare_pitch_data(mocapEuler,baseEuler)

	plt.show()

def get_data(data, bag):
	mocapQuat = data.get_mocap(bag)
	baseEuler = data.get_base_euler(bag)
	
	return baseEuler,mocapQuat

def quat2euler(quatStruct):
	quat = np.array(quatStruct.quat)
	euler = R.from_quat(quat.T).as_euler('xyz').T
	eulerStruct = Euler(quatStruct.time,euler)
	return eulerStruct

def compare_roll_data(mocapEuler,estEuler):
	fig_num = 1
	plot_2(fig_num, mocapEuler.time, mocapEuler.euler[0], 'mocap roll', estEuler.time, estEuler.euler[0], 'est roll')

def compare_pitch_data(mocapEuler,estEuler):
	fig_num = 2
	plot_2(fig_num, mocapEuler.time, mocapEuler.euler[1], 'mocap pitch', estEuler.time, estEuler.euler[1], 'est pitch')

def plot_2(fig_num, t_x, x, xlabel, t_y, y, ylabel):

	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.legend(loc = "upper right")

class Euler:
	def __init__(self,time,euler):
		self.time = time
		self.euler = euler

if __name__ == '__main__':
	main()
