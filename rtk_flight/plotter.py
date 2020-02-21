from rosbag_parser import Parser
import matplotlib.pyplot as plt
from IPython.core.debugger import set_trace
import rosbag
import numpy as np

def main():
	
	parser = Parser()

	filename = 'land_2-19.bag'
	bag = rosbag.Bag('../../data/mocap/' + filename)

	vals = parser.get_variables(bag)
	bag.close

	truth_name = 'odom'
	truth = vals.odom
	ideal_name = 'high level command'
	ideal = vals.hl_cmd
	plot_compare_position(truth_name, truth, ideal_name, ideal)
	plot_compare_position(truth_name, truth, 'mocap', vals.drone)

	bool_name = 'is_flying'
	boolean = vals.is_flying
	plot_bool(bool_name, boolean)

	#TODO boolean function isn't working
	# bool_name = 'is_landing'
	# boolean = vals.is_landing
	# plot_bool(bool_name, boolean)

def plot_compare_position(truth_name, truth, ideal_name, ideal):

	truth_time = np.array(truth.sec)+np.array(truth.nsec)*1E-9
	ideal_time = np.array(ideal.sec)+np.array(ideal.nsec)*1E-9

	fig1, sub = plt.subplots(3)
	fig1.suptitle(truth_name + " vs. " + ideal_name)
	#compare x truth to x ideal
	sub[0].plot(truth_time, truth.position[0], label = truth_name + " x")
	sub[0].plot(ideal_time, ideal.position[0], label = ideal_name + " x")
	sub[0].legend(loc = "upper right")
	sub[0].set_xlabel('t [s]')
	sub[0].set_ylabel('x pos')

	#compare y truth to y ideal
	sub[1].plot(truth_time, truth.position[1], label = truth_name + " y")
	sub[1].plot(ideal_time, ideal.position[1], label = ideal_name + " y")
	sub[1].legend(loc = "upper right")
	sub[1].set_xlabel('t [s]')
	sub[1].set_ylabel('y pos')
	
	#compare z truth to z ideal
	sub[2].plot(truth_time, truth.position[2], label = truth_name + " z")
	sub[2].plot(ideal_time, ideal.position[2], label = ideal_name + " z")
	sub[2].legend(loc = "upper right")
	sub[2].set_xlabel('t [s]')
	sub[2].set_ylabel('z pos')

def plot_bool(bool_name, boolean):

	new_bool = []
	for i in range(len(boolean)):
		if boolean == True:
			new_bool.append(1)
		elif boolean == False:
			new_bool.append(0)
		# else:
		# 	print('bad boolean')
		set_trace()
	#compare x truth to x ideal
	plt.plot(new_bool)

if __name__ == '__main__':
	main()
