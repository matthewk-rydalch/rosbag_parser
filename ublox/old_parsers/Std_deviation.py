from IPython.core.debugger import set_trace
import rosbag
import pickle
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
from rosbag_parser import Parser


def main():
	#from original test
	filename1 = 'data.bag'
	bag1 = rosbag.Bag('../../data/rod/250cm_lazy/' + filename1)

	data = Parser()

	var1 = data.get_variables(bag1, filename1)
	bag1.close()

	time1 = 60*np.array(var1.minute)+np.array(var1.sec)

	plotter(var1.relPoslength, time1)


# def remove_blanks(vals):
# 	bad_ind = []
# 	#if RTK isn't being used, maybe use year instead of flags
# 	length = len(vals.year)
# 	for i in range(length):
# 		if vals.year[i] == 2018:
# 			bad_ind.append(i)
#
# 	fields = vals._fields
# 	strike = 0
# 	for f in fields:
# 		if len(getattr(vals,f)) == length:
# 			for j in bad_ind:
# 				del getattr(vals,f)[j-strike]
# 				strike = strike+1
# 		strike = 0
#
# 	return(bad_ind, vals)

def plotter(length, time1):

	fig1 = plt.figure()
	plt.plot(time1, length, label = "rosbag")
	plt.legend(loc='upper right', prop={'size': 16}, frameon=False)
	plt.xlabel('time (s)')
	plt.ylabel('longitude (deg?)')
	plt.show


# def error_calc(NED, time1, lla2, time2):
#
# 	NED = np.array(NED)
# 	north = NED[:,0]
# 	east = NED[:,1]
# 	altitude_1 = NED[:,2]
#
# 	lla2 = np.array(lla2)
# 	longitude_2 = lla2[:,0]
# 	latitude_2 = lla2[:,1]
# 	altitude_2 = lla2[:,2]
#
# 	longitude_e = []
# 	latitude_e = []
# 	altitude_e = []
#
# 	strike = 0
# 	set_trace()
# 	for i in range(len(time1)):
# 		if time1[i] == time2[i-strike]:
# 			longitude_e.append(longitude_2[i-strike]-north[i])
# 			latitude_e.append(latitude_2[i-strike]-east[i])
# 			altitude_e.append(altitude_2[i-strike]-altitude_1[i])
# 		else:
# 			strike = strike+1
#
# 	error = np.array([[longitude_e], [latitude_e], [altitude_e]])
#
# 	length = len(longitude_e)
# 	lo_av_e = sum(longitude_e)/length
# 	la_av_e = sum(latitude_e)/length
# 	al_av_e = sum(altitude_e)/length
#
# 	return error, lo_av_e, la_av_e, al_av_e, strike

if __name__ == '__main__':
	rbag, bad_ind, vals, error, lo_av_e, la_av_e, al_av_e, strike = main()