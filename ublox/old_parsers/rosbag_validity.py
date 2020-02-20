#This file plots values red that are both fixed and valid

from IPython.core.debugger import set_trace
from importlib import reload
import rosbag
import matplotlib.pyplot as plt
import numpy as np
# import rosbag_parser

from rosbag_parser import get_variables

# reload(rosbag_parser)

filename = 'aug1_utc_walk_01.bag'
bag = rosbag.Bag('../../../data/UTC_test/' + filename)
# bag = rosbag.Bag(filename)
variables = get_variables(bag, filename)
set_trace()
bag.close()
nsecs_rel = np.array([i*1E-9 for i in variables.nsecs_rel])
secs_rel = np.array(varialbes.secs_rel)
relPosNED = np.array(varialbes.relPosNED)
# nsecs_pos = np.array([i*1E-9 for i in nsecs_pos])
# secs_pos = np.array(secs_pos)
flags = varialbes.flags
relPosLength = np.array(variables.relPosLength)
# relPosHPLength = np.array(relPosHPLength)
# Length = relPosLength+relPosHPLength
Length = relPosLength

north = []
east = []
down = []
northHP = []
eastHP = []
downHP = []
North = []
East = []
Down = []

# set_trace()
time_rel = secs_rel+nsecs_rel-secs_rel[0]-nsecs_rel[0]
# time_pos = secs_pos+nsecs_pos-secs_pos[0]-nsecs_pos[0]
size_rel = len(time_rel)
# size_pos = len(time_pos)
lat = []
lon = []
alt = []
# for i in range(0,size_pos-1):
	# lat.append(lla[i][0])
	# lon.append(lla[i][1])
	# alt.append(lla[i][2])

for i in range(0,size_rel):
	north.append(variables.relPosNED[i][0])
	east.append(varialbes.relPosNED[i][1])
	down.append(variables.relPosNED[i][2])
	# northHP.append(relPosNEDHP[i][0])
	# eastHP.append(relPosNEDHP[i][1])
	# downHP.append(relPosNEDHP[i][2])
	North.append(north[i])#+northHP[i])
	East.append(east[i])#+eastHP[i])
	Down.append(down[i])#+downHP[i])

valid_time = []
valid_dis = []
invalid_time = []
invalid_dis = []

True_value = 2.50
Truth = [size_rel]
Truth = [True_value]*size_rel

for i in range(0,size_rel):
	#if moving base
	if flags[i] == 503 or flags[i] == 247 or flags[i] == 119 or flags[i] == 55 or flags[i] == 375 or flags[i] == 311 or flags[i] == 439:
		valid_time.append(time_rel[i])
		valid_dis.append(Length[i])
	else:
		invalid_time.append(time_rel[i])
		invalid_dis.append(Length[i])
	# #if stationary base
	# if flags[i] == 471 or flags[i] == 215 or flags[i] == 87 or flags[i] == 23 or flags[i] == 343 or flags[i] == 279 or flags[i] == 407:
	# 	valid_time.append(time_rel[i])
	# 	valid_dis.append(Length[i])
	# else:
	# 	invalid_time.append(time_rel[i])
	# 	invalid_dis.append(Length[i])
#find time to valid
if len(valid_time) != 0:
	time_to_valid = valid_time[0]
	#find average valid length
	valid_len = len(valid_dis)
	average_length = 100*sum(valid_dis)/valid_len #in cm

	#find average valid maginitude error
	error = [abs(x-True_value) for x in valid_dis]
	average_error = 100*sum(error)/valid_len #in cm
else:
	time_to_valid = 1000
	invalid_len = len(invalid_dis)
	average_length = 100*sum(invalid_dis)/invalid_len #in cm
	#find average valid maginitude error
	error = [abs(x-True_value) for x in invalid_dis]
	average_error = 100*sum(error)/invalid_len #in cm

fig = plt.figure()
plt.plot(time_rel, Truth, color = "black", label ="Truth")
plt.scatter(valid_time, valid_dis, s=1, color="red", label="valid lengths")
plt.scatter(invalid_time, invalid_dis, s=1, color="blue", label="invalid lengths")
plt.legend(loc='upper right', prop={'size': 16}, frameon=False)
plt.xlabel('time (s)')
plt.ylabel('Relative Distance (m)')
#plt.figtext(.8, .5, 'Time to valid = %d \n Average Length = %d' % (time_to_valid, average_length))
plt.figtext(.5, .5, 'Time to valid = %f s \nAverage Length = %f cm \nAverage Error = %f cm' % (time_to_valid, average_length, average_error))
fig.suptitle(foldername + '\ntime vs. relative distance')
# fig.savefig('../../../data/' + foldername + '/Distance')

if len(valid_time) != 0:
	Truth_cm = [i*100 for i in Truth]
	valid_dis_cm = [i*100 for i in valid_dis]
	fig2 = plt.figure()
	plt.plot(time_rel, Truth_cm, color = "black", label ="Truth")
	plt.scatter(valid_time, valid_dis_cm, s=1, color="red", label="valid lengths")
	plt.legend(loc='upper left', prop={'size': 16}, frameon=False)
	plt.xlabel('time (s)')
	plt.ylabel('Relative Distance (cm)')
	fig2.suptitle(foldername + '(valid solutions only)\ntime vs. relative distance')
	# fig2.savefig('../../../data/' + foldername + '/valid Distance')

mag = np.sqrt(np.square(North)+np.square(East)+np.square(Down))
fig3 = plt.figure()
plt.plot(time_rel, Truth, color = "black", label ="Truth")
plt.plot(time_rel, mag, color="yellow", label="Magnitude")
plt.plot(time_rel, North, color="red", label="T")
plt.plot(time_rel, North, color="red", label="North")
plt.plot(time_rel, East, color="blue", label="East")
plt.plot(time_rel, Down, color="green", label="Down")
plt.legend(loc='lower left', prop={'size': 10}, frameon=False)
plt.xlabel('time (s)')
plt.ylabel('Length (m)')
fig3.suptitle(foldername + '\ntime vs. north east down')
# fig3.savefig('../../../data/' + foldername + '/NED')
plt.show()
