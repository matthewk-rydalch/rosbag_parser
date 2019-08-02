from IPython.core.debugger import set_trace
from importlib import reload
import rosbag
import matplotlib.pyplot as plt
import numpy as np

from collections import namedtuple
from rosbag_parser import Parser

def main():
	parse = Parser()
	precision = Precision()

	# import variables
	numOfFiles = 7
	Filename = ['none']*numOfFiles
	data = [0]*numOfFiles
	variables = [0]*numOfFiles
	legend_names = [0]*numOfFiles
	#need to have as many colors as there are filnames
	colors = ['red', 'yellow', 'black', 'orange', 'green', 'blue', 'purple']
	plotname = 'aug1 utc walk precision test\nEast vs. North'
	figname = 'aug1_utc_walk_precision.jpeg'
	legend_names[0] = 'walk 1'
	legend_names[1] = 'walk 2'
	legend_names[2] = 'walk 3'
	legend_names[3] = 'walk 4'
	legend_names[4] = 'walk 5'
	legend_names[5] = 'walk 6'
	legend_names[6] = 'walk 7'
	Filename[0] = 'aug1_utc_walk_01.bag'
	Filename[1] = 'aug1_utc_walk_02.bag'
	Filename[2] = 'aug1_utc_walk_03.bag'
	Filename[3] = 'aug1_utc_walk_04.bag'
	Filename[4] = 'aug1_utc_walk_05.bag'
	Filename[5] = 'aug1_utc_walk_06.bag'
	Filename[6] = 'aug1_utc_walk_07.bag'

	path = '../../../data/UTC_test/'

	for i in range(numOfFiles-1):
		[data[i], variables[i]] = precision.calc(path, Filename[i], parse)
	
	precision.plot_on(data, numOfFiles, plotname, colors, legend_names, figname, path)

	return data, variables


class Precision:
	def calc(self, path, filename, parse):
		bag = rosbag.Bag(path + filename)
		variables = parse.get_variables(bag, filename)
		flags = variables.flags

		north = []
		east = []
		down = []
		northhp = []
		easthp = []
		downhp = []
		North = []
		East = []
		Down = []

		# split fixed and float
		#fixed means that RTK is in fix mode and that the solution is validl
		fix_N = []
		float_N = []
		fix_E = []
		float_E = []
		fix_D = []
		float_D = []

		size = len(flags)

		for i in range(0,size):
			north.append(variables.relPosNED[i][0])
			east.append(variables.relPosNED[i][1])
			down.append(variables.relPosNED[i][2])
			northhp.append(variables.relPosNEDHP[i][0])
			easthp.append(variables.relPosNEDHP[i][1])
			downhp.append(variables.relPosNEDHP[i][2])
			North.append(north[i]+northhp[i])
			East.append(east[i]+easthp[i])
			Down.append(down[i]+downhp[i])

		# # for mobile base mode
		# for i in range(0,size):
		# 	if flags[i] == 503 or flags[i] == 247 or flags[i] == 119 or flags[i] == 55 or flags[i] == 375 or flags[i] == 311 or flags[i] == 439:
		# 		fix_N.append(North[i])
		# 		fix_E.append(East[i])
		# 		fix_D.append(Down[i])
		# 	else:
		# 		float_N.append(North[i])
		# 		float_E.append(East[i])
		# 		float_D.append(Down[i])

		# for stationary base mode
		for i in range(0,size):
			if flags[i] == 471 or flags[i] == 215 or flags[i] == 87 or flags[i] == 23 or flags[i] == 343 or flags[i] == 279 or flags[i] == 407:
				fix_N.append(North[i])
				fix_E.append(East[i])
				fix_D.append(Down[i])
			else:
				float_N.append(North[i])
				float_E.append(East[i])
				float_D.append(Down[i])
		
		MyStruct = namedtuple("mystruct", "flags, North, East, \
		Down, fix_N, float_N, fix_E, float_E, fix_D, float_D")

		data = MyStruct(flags, North, East, Down, fix_N, float_N, fix_E, float_E, fix_D, float_D)

		return data, variables

	def plot_on(self, data, numOfTests, plotname, colors, legend_names, figname, path):

		fix_N = [0]*numOfTests
		float_N = [0]*numOfTests
		fix_E = [0]*numOfTests
		float_E = [0]*numOfTests

		fig = plt.figure()		
		for i in range(numOfTests-1):
			fix_N[i] = data[i].fix_N
			float_N[i] = data[i].float_N
			fix_E[i] = data[i].fix_E
			float_E[i] = data[i].float_E
			plt.plot(fix_E[i], fix_N[i], color = colors[i], linewidth = 1, label = legend_names[i])
			plt.scatter(float_E[i], float_N[i], s = 10, color = colors[i])

		plt.legend(bbox_to_anchor=(1, .4), prop={'size': 8}, frameon=True)
		plt.xlabel('East (m)')
		plt.ylabel('North (m)')
		plt.figtext(.45, .15, 'Dots are data that was not fixed in RTK')
		fig.suptitle(plotname)
		# fig.savefig(path + figname)

		plt.show()

if __name__ == '__main__':
	[data, variables] = main()