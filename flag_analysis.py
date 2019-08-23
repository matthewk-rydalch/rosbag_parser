
from IPython.core.debugger import set_trace
from importlib import reload
import rosbag
import matplotlib.pyplot as plt
import numpy as np

from collections import namedtuple
from rosbag_parser import Parser
from statistics import mode

def main():
	numOfFiles = 6
	Filename = ['none']*numOfFiles
	vals = [0]*numOfFiles

	Filename[0] = 'MB_rover1.bag'
	Filename[1] = 'MB_rover2.bag'
	Filename[2] = 'MB_rover3.bag'
	Filename[3] = 'MB_base1.bag'
	Filename[4] = 'MB_base2.bag'
	Filename[5] = 'MB_base3.bag'

	path = '../../../data/08_22_walk/'

	for i in range(0,numOfFiles):
		vals[i] = calc(Filename[i], path)

	return vals

def calc(filename, pathname):
	fix_num = 0
	valid_num = 0

	parse = Parser()
	bag = rosbag.Bag(pathname + filename)
	variables = parse.get_variables(bag, filename)

	flags = variables.flags
	nano = variables.nano
	sec = variables.sec
	minute = variables.minute
	hr = variables.hour
	size = len(sec)
	time = [0]*size
	max_gap = 0
	gap = [0]*(size)

	for i in range(0,size):
		time[i] = nano[i]*1e-9+sec[i]+minute[i]*60+hr[i]*3600

	for i in range(1,size):
		gap[i] = time[i]-time[i-1]
		if gap[i]>max_gap:
			max_gap = gap[i]

	gap_r = [0]*size
	for i in range(0,size):
		gap_r[i] = round(gap[i],2)

	gap_mode = mode(gap_r)

	for x in flags:
		if x == 311:
			fix_num = fix_num+1
			valid_num = valid_num+1
		if x == 179:
			fix_num = fix_num+1

	fix_per = fix_num/size*100
	valid_per = valid_num/size*100

	hz = size/(time[size-1]-time[0])

	MyStruct = namedtuple("mystruct", ("fix_num", "fix_per", "valid_num", "valid_per", "time", "hz", "gap", "max_gap", "gap_mode"))
	vals = MyStruct(fix_num, fix_per, valid_num, valid_per, time, hz, gap, max_gap, gap_mode)

	return vals

if __name__ == '__main__':
    vals = main()
