from IPython.core.debugger import set_trace
from importlib import reload
import rosbag
import matplotlib.pyplot as plt
import numpy as np

from collections import namedtuple
from sim_parser import Parser
from statistics import mode

def main():
	filename = '_2019-09-06-10-46-56.bag'
	path = '../../../data/holodeck_sim/'
	vals = plot(filename, path)

	return vals


def plot(filename, pathname):
	parse = Parser()
	bag = rosbag.Bag(pathname + filename)
	variables = parse.get_variables(bag, filename)

	sec = variables.sec
	nsec = variables.nsec
	X = variables.X
	Y = variables.Y
	Z = variables.Z
	time = [0]*len(sec)
	for i in range(0,len(sec)):
		time[i] = sec[i] + nsec[i]*1e-9

	sec_c = [0]*(2*len(variables.sec_c))
	Xc = [0]*(2*len(variables.sec_c))
	Yc = [0]*(2*len(variables.sec_c))
	Zc = [0]*(2*len(variables.sec_c))
	for i in range(0,len(variables.sec_c)):
		sec_c[2*i] = variables.sec_c[i]
		if i < len(variables.sec_c)-1:
			sec_c[2*i+1] = variables.sec_c[i+1]
		else:
			sec_c[2*i+1] = time[len(time)-1]

		Xc[2*i] = variables.Xc[i]
		Xc[2*i+1] = variables.Xc[i]		
		Yc[2*i] = variables.Yc[i]
		Yc[2*i+1] = variables.Yc[i]		
		Zc[2*i] = variables.Fc[i]
		Zc[2*i+1] = variables.Fc[i]		

	fig = plt.figure(1)
	plt.plot(sec_c, Xc, color = "blue", linewidth = 1, label = "Xc")
	plt.plot(time, X, color = "red", linewidth = 1, label = "X")
	# plt.xlim([-5, 165])
	# plt.ylim([-.5, 14.5])
	plt.legend(bbox_to_anchor=(1, .4), prop={'size': 8}, frameon=True)
	plt.xlabel('Time (s)')
	plt.ylabel('X Position')
	fig.suptitle('X')
	# fig.savefig(path + filename + x')
	plt.show()

	fig = plt.figure(2)
	plt.plot(sec_c, Yc, color = "blue", linewidth = 1, label = "Yc")
	plt.plot(time, Y, color = "red", linewidth = 1, label = "Y")
	# plt.xlim([-5, 165])
	# plt.ylim([-7.5, 7.5])
	plt.legend(bbox_to_anchor=(1, .4), prop={'size': 8}, frameon=True)
	plt.xlabel('Time (s)')
	plt.ylabel('Y Position')
	fig.suptitle('Y')
	# fig.savefig(path + filename + 'y')

	fig = plt.figure(3)
	plt.plot(sec_c, Zc, color = "blue", linewidth = 1, label = "Zc")
	plt.plot(time, Z, color = "red", linewidth = 1, label = "Z")
	# plt.xlim([-5, 165])
	# plt.ylim([-50, 5])
	plt.legend(bbox_to_anchor=(1, .4), prop={'size': 8}, frameon=True)
	plt.xlabel('Time (s)')
	plt.ylabel('Z Position')
	fig.suptitle('Z')
	# fig.savefig(path + filename + 'z')

	MyStruct = namedtuple("mystruct", ("sec_c", "Xc", "Yc", "Zc", "Fc", "sec", "nsec", "time", "X", "Y", "Z"))
	vals = MyStruct(variables.sec_c, variables.Xc, variables.Yc, variables.Zc, variables.Fc, sec, nsec, time, X, Y, Z)

	return vals	

if __name__ == '__main__':
    vals = main()