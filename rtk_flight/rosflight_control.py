from rosbag_parser import Parser
import matplotlib.pyplot as plt
# from IPython.core.debugger import set_trace
import rosbag
import numpy as np
from collections import namedtuple

def main():
	
	data = Parser()

	filename = 'hover_no_noise.bag'
	bag = rosbag.Bag('../../data/mocap/' + filename)

	command, attitudeEuler = get_data(data, bag)
	offset = 23.0
	command, attitudeEuler = align_times(command, attitudeEuler, offset)
	plot_2(1,command.time,command.roll,'command roll',attitudeEuler.time,attitudeEuler.roll,'actual roll')
	plot_2(2, command.time, command.pitch, 'command pitch', attitudeEuler.time, attitudeEuler.pitch, 'actual pitch')

def get_data(data, bag):

	command = data.get_command(bag)
	attitudeEuler = data.get_attitude_euler(bag)
	bag.close()

	return command, attitudeEuler

def align_times(cmd,att,offset):
	cmd.time = cmd.time-cmd.time[0]
	att.time = att.time-att.time[0]-offset
	return cmd, att

def plot_2(fig_num, t_x, x, xlabel, t_y, y, ylabel):

	plt.figure(fig_num)
	plt.plot(t_x, x, label = xlabel)
	plt.plot(t_y, y, label = ylabel)
	plt.legend(loc = "upper right")
	plt.show()


if __name__ == '__main__':
	main()
