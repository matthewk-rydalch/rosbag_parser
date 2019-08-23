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
	numOfFiles = 6
	Filename = ['none']*numOfFiles
	data = [0]*numOfFiles
	variables = [0]*numOfFiles
	legend_names = [0]*numOfFiles
	#need to have as many colors as there are filnames
	colors = ['red', 'yellow', 'black', 'orange', 'green', 'blue']#, 'purple', 'pink', 'brown', 'gray']
	plotname = '08/22/19 Precision Test\nEast vs. North'
	# figname = '08_22_19_precision.jpeg'
	figname = 'MB_0822.jpeg'

	legend_names[0] = 'MB rover 1'
	legend_names[1] = 'MB rover 2'
	legend_names[2] = 'MB rover 3'
	legend_names[3] = 'MB base 1'
	legend_names[4] = 'MB base 2'
	legend_names[5] = 'MB base 3'

	Filename[0] = 'MB_rover1.bag'
	Filename[1] = 'MB_rover2.bag'
	Filename[2] = 'MB_rover3.bag'
	Filename[3] = 'MB_base1.bag'
	Filename[4] = 'MB_base2.bag'
	Filename[5] = 'MB_base3.bag'

	path = '../../../data/08_22_walk/'

	fix_N = []
	fix_E = []
	fix_D = []
	nval_N = []
	nval_E = []
	nval_D = []
	float_N = []
	float_E = []
	float_D = []
	for i in range(0,numOfFiles-3):
		print('count', i)
		[data[i], variables[i]] = precision.calc(path, Filename[i], parse)
		fix_N.append(data[i].fix_N)
		fix_E.append(data[i].fix_E)
		fix_D.append(data[i].fix_D)
		nval_N.append(data[i].nval_N)
		nval_E.append(data[i].nval_E)
		nval_D.append(data[i].nval_D)
		float_N.append(data[i].float_N)
		float_E.append(data[i].float_E)
		float_D.append(data[i].float_D)
	for i in range(numOfFiles-3,numOfFiles):
		print('count', i)
		[data[i], variables[i]] = precision.calc(path, Filename[i], parse)
		fix_n = data[i].fix_N
		fix_e = data[i].fix_E
		fix_d = data[i].fix_D
		nval_n = data[i].nval_N
		nval_e = data[i].nval_E
		nval_d = data[i].nval_D
		float_n = data[i].float_N
		float_e = data[i].float_E
		float_d = data[i].float_D
		fix_n_neg = [-x for x in fix_n]
		fix_e_neg = [-x for x in fix_e]
		fix_d_neg = [-x for x in fix_d]
		nval_n_neg = [-x for x in nval_n]
		nval_e_neg = [-x for x in nval_e]
		nval_d_neg = [-x for x in nval_d]
		float_n_neg = [-x for x in float_n]
		float_e_neg = [-x for x in float_e]
		float_d_neg = [-x for x in float_d]
		fix_N.append(fix_n_neg)
		fix_E.append(fix_e_neg)
		fix_D.append(fix_d_neg)
		nval_N.append(nval_n_neg)
		nval_E.append(nval_e_neg)
		nval_D.append(nval_d_neg)
		float_N.append(float_n_neg)
		float_E.append(float_e_neg)
		float_D.append(float_d_neg)
	MyStruct = namedtuple("mystruct", "fix_N, fix_E, fix_D, nval_N, nval_E, nval_D, float_N, float_E, float_D")
	NED = MyStruct(fix_N, fix_E, fix_D, nval_N, nval_E, nval_D, float_N, float_E, float_D)
	precision.plot_on(NED, numOfFiles, plotname, colors, legend_names, figname, path)

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
		nval_N = []
		float_N = []
		fix_E = []
		nval_E = []
		float_E = []
		fix_D = []
		nval_D = []
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
		for i in range(0,size):
			if flags[i] == 503 or flags[i] == 247 or flags[i] == 119 or flags[i] == 55 or flags[i] == 375 or flags[i] == 311 or flags[i] == 439:
				fix_N.append(North[i])
				fix_E.append(East[i])
				fix_D.append(Down[i])
			elif flags[i] == 179:
				nval_N.append(North[i])
				nval_E.append(East[i])
				nval_D.append(Down[i])
			else:
				float_N.append(North[i])
				float_E.append(East[i])
				float_D.append(Down[i])

		# # for stationary base mode
		# for i in range(0,size):
		# 	if flags[i] == 471 or flags[i] == 215 or flags[i] == 87 or flags[i] == 23 or flags[i] == 343 or flags[i] == 279 or flags[i] == 407:
		# 		fix_N.append(North[i])
		# 		fix_E.append(East[i])
		# 		fix_D.append(Down[i])
		# 	else:
		# 		float_N.append(North[i])
		# 		float_E.append(East[i])
		# 		float_D.append(Down[i])

		# for comparing both
		# for i in range(0,size):
		# 	if flags[i] == 471 or flags[i] == 215 or flags[i] == 87 or flags[i] == 23 or flags[i] == 343 or flags[i] == 279 or flags[i] == 407 or flags[i] == 503 or flags[i] == 247 or flags[i] == 119 or flags[i] == 55 or flags[i] == 375 or flags[i] == 311 or flags[i] == 439:
		# 		fix_N.append(North[i])
		# 		fix_E.append(East[i])
		# 		fix_D.append(Down[i])
		# 	else:
		# 		float_N.append(North[i])
		# 		float_E.append(East[i])
		# 		float_D.append(Down[i])

		MyStruct = namedtuple("mystruct", "flags, North, East, \
		Down, fix_N, nval_N, float_N, fix_E, nval_E, float_E, fix_D, nval_D, float_D")

		data = MyStruct(flags, North, East, Down, fix_N, nval_N, float_N, fix_E, nval_E, float_E, fix_D, nval_D, float_D)

		return data, variables

	def plot_on(self, NED, numOfTests, plotname, colors, legend_names, figname, path):

		fix_N = [0]*numOfTests
		nval_N = [0]*numOfTests
		float_N = [0]*numOfTests
		fix_E = [0]*numOfTests
		nval_E = [0]*numOfTests
		float_E = [0]*numOfTests

		fig = plt.figure()		
		for i in range(0, 6):
			fix_N[i] = NED.fix_N[i]
			nval_N[i] = NED.nval_N[i]
			float_N[i] = NED.float_N[i]
			fix_E[i] = NED.fix_E[i]
			nval_E[i] = NED.nval_E[i]
			float_E[i] = NED.float_E[i]
			# plt.plot(fix_E[i], fix_N[i], color = colors[i], label = legend_names[i])
			plt.scatter(fix_E[i], fix_N[i], s = 1, color = colors[i], label = legend_names[i])
			plt.scatter(nval_E[i], nval_N[i], s = 10, marker='^', color = colors[i])
			plt.scatter(float_E[i], float_N[i], s = 20, marker='o', color = colors[i])
		# i = 5
		# plt.scatter(fix_E[i], fix_N[i], s = 1, color = colors[i], label = legend_names[i])
		# plt.scatter(nval_E[i], nval_N[i], s = 10, marker='^', color = colors[i])
		# plt.scatter(float_E[i], float_N[i], s = 20, marker='o', color = colors[i])
		plt.legend(bbox_to_anchor=(1, .6), prop={'size': 8}, frameon=True)
		plt.xlabel('East (m)')
		plt.ylabel('North (m)')
		# plt.figtext(.45, .15, 'Dots are data that was not fixed in RTK')
		fig.suptitle(plotname)
		fig.savefig(path + figname)

		plt.show()

if __name__ == '__main__':
	[data, variables] = main()