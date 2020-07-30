from IPython.core.debugger import set_trace
import rosbag
import pickle
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
from rosbag_parser import Parser


def main():
	#from original test
	filename1 = 'standard1.bag'
	#from binary data
	filename2 = 'binary1_slow.bag'
	bag1 = rosbag.Bag('../../../data/rtk_tests/standard_binary_tests/' + filename1)
	bag2 = rosbag.Bag('../../../data/rtk_tests/standard_binary_tests/' + filename2)

	data = Parser()

	var1 = data.get_variables(bag1, filename1)
	bag1.close()

	var2 = data.get_variables(bag2, filename2)
	bag2.close()

	set_trace()
	bad_ind, dvar2 = remove_blanks(var2)

	time1 = 60*np.array(var1.minute)+np.array(var1.sec)
	time2 = 60*np.array(dvar2.minute)+np.array(dvar2.sec)

	plotter(var1.lla, time1, dvar2.lla, time2)

	error, lo_av_e, la_av_e, al_av_e, strike = error_calc(var1.lla, time1, dvar2.lla, time2)

	return var1, bad_ind, dvar2, error, lo_av_e, la_av_e, al_av_e, strike


def remove_blanks(vals):
	bad_ind = []
	#if RTK isn't being used, maybe use year instead of flags
	length = len(vals.year)
	for i in range(length):
		if vals.year[i] == 2018:
			bad_ind.append(i)

	fields = vals._fields
	strike = 0
	for f in fields:
		if len(getattr(vals,f)) == length:
			for j in bad_ind:
				del getattr(vals,f)[j-strike]
				strike = strike+1
		strike = 0

	return(bad_ind, vals)

def plotter(lla1, time1, lla2, time2):


	lla1 = np.array(lla1)
	longitude_1 = lla1[:,0]
	latitude_1 = lla1[:,1]
	altitude_1 = lla1[:,2]

	lla2 = np.array(lla2)
	longitude_2 = lla2[:,0]
	latitude_2 = lla2[:,1]
	altitude_2 = lla2[:,2]

	fig1 = plt.figure()
	plt.plot(time1, longitude_1, label = "rosbag")
	plt.plot(time2, longitude_2, label = "binary")
	plt.legend(loc='upper right', prop={'size': 16}, frameon=False)
	plt.xlabel('time (s)')
	plt.ylabel('longitude (deg?)')
	plt.show
	fig2 = plt.figure()
	plt.plot(time1, latitude_1, label = "rosbag")
	plt.plot(time2, latitude_2, label = "binary")
	plt.legend(loc='upper right', prop={'size': 16}, frameon=False)
	plt.xlabel('time (s)')
	plt.ylabel('longitude (deg?)')
	plt.show
	fig3 = plt.figure()
	plt.plot(time1, altitude_1, label = "rosbag")
	plt.plot(time2, altitude_2, label = "binary")
	plt.legend(loc='upper right', prop={'size': 16}, frameon=False)
	plt.xlabel('time (s)')
	plt.ylabel('longitude (deg?)')
	plt.show

def error_calc(lla1, time1, lla2, time2):

	lla1 = np.array(lla1)
	longitude_1 = lla1[:,0]
	latitude_1 = lla1[:,1]
	altitude_1 = lla1[:,2]

	lla2 = np.array(lla2)
	longitude_2 = lla2[:,0]
	latitude_2 = lla2[:,1]
	altitude_2 = lla2[:,2]

	longitude_e = []
	latitude_e = []
	altitude_e = []

	strike = 0
	set_trace()
	for i in range(len(time1)):
		if time1[i] == time2[i-strike]:
			longitude_e.append(longitude_2[i-strike]-longitude_1[i])
			latitude_e.append(latitude_2[i-strike]-latitude_1[i])
			altitude_e.append(altitude_2[i-strike]-altitude_1[i])
		else:
			strike = strike+1

	error = np.array([[longitude_e], [latitude_e], [altitude_e]])

	length = len(longitude_e)
	lo_av_e = sum(longitude_e)/length
	la_av_e = sum(latitude_e)/length
	al_av_e = sum(altitude_e)/length

	return error, lo_av_e, la_av_e, al_av_e, strike

if __name__ == '__main__':
	rbag, bad_ind, vals, error, lo_av_e, la_av_e, al_av_e, strike = main()