from IPython.core.debugger import set_trace
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np
import rosbag_parser

reload(rosbag_parser)

nsecs_rel = np.array([i*1E-9 for i in rosbag_parser.nsecs_rel])
secs_rel = np.array(rosbag_parser.secs_rel)
relPosNED = np.array(rosbag_parser.relPosNED)
# nsecs_pos = np.array([i*1E-9 for i in rosbag_parser.nsecs_pos])
# secs_pos = np.array(rosbag_parser.secs_pos)
flags = rosbag_parser.flags
relPosLength = np.array(rosbag_parser.relPosLength)
# relPosHPLength = np.array(rosbag_parser.relPosHPLength)
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
	# lat.append(rosbag_parser.lla[i][0])
	# lon.append(rosbag_parser.lla[i][1])
	# alt.append(rosbag_parser.lla[i][2])

for i in range(0,size_rel):
	north.append(rosbag_parser.relPosNED[i][0])
	east.append(rosbag_parser.relPosNED[i][1])
	down.append(rosbag_parser.relPosNED[i][2])
	# northHP.append(rosbag_parser.relPosNEDHP[i][0])
	# eastHP.append(rosbag_parser.relPosNEDHP[i][1])
	# downHP.append(rosbag_parser.relPosNEDHP[i][2])
	North.append(north[i])#+northHP[i])
	East.append(east[i])#+eastHP[i])
	Down.append(down[i])#+downHP[i])

fix_time = []
fix_dis = []
float_time = []
float_dis = []

True_value = 2.50
Truth = [size_rel]
Truth = [True_value]*size_rel

for i in range(0,size_rel):
	# if flags[i] == 375 or flags[i] == 179 or flags[i] == 311 or flags[i] == 243 or flags[i] == 279:
	if flags[i] == 179:
		fix_time.append(time_rel[i])
		fix_dis.append(Length[i])
	else:
		float_time.append(time_rel[i])
		float_dis.append(Length[i])

#find time to fix
if len(fix_time) != 0:
	time_to_fix = fix_time[0]
	#find average fixed length
	fix_len = len(fix_dis)
	average_length = 100*sum(fix_dis)/fix_len #in cm

	#find average fixed maginitude error
	error = [abs(x-True_value) for x in fix_dis]
	average_error = 100*sum(error)/fix_len #in cm
else:
	time_to_fix = 1000
	float_len = len(float_dis)
	average_length = 100*sum(float_dis)/float_len #in cm
	#find average fixed maginitude error
	error = [abs(x-True_value) for x in float_dis]
	average_error = 100*sum(error)/float_len #in cm

fig = plt.figure()
plt.plot(time_rel, Truth, color = "black", label ="Truth")
plt.scatter(fix_time, fix_dis, s=1, color="red", label="fixed lengths")
plt.scatter(float_time, float_dis, s=1, color="blue", label="float lengths")
plt.legend(loc='upper right', prop={'size': 16}, frameon=False)
plt.xlabel('time (s)')
plt.ylabel('Relative Distance (m)')
#plt.figtext(.8, .5, 'Time to Fix = %d \n Average Length = %d' % (time_to_fix, average_length))
plt.figtext(.5, .5, 'Time to Fix = %f s \nAverage Length = %f cm \nAverage Error = %f cm' % (time_to_fix, average_length, average_error))
fig.suptitle(rosbag_parser.foldername + '\ntime vs. relative distance')
# fig.savefig('../../../data/' + rosbag_parser.foldername + '/Distance')

if len(fix_time) != 0:
	Truth_cm = [i*100 for i in Truth]
	fix_dis_cm = [i*100 for i in fix_dis]
	fig2 = plt.figure()
	plt.plot(time_rel, Truth_cm, color = "black", label ="Truth")
	plt.scatter(fix_time, fix_dis_cm, s=1, color="red", label="fixed lengths")
	plt.legend(loc='upper left', prop={'size': 16}, frameon=False)
	plt.xlabel('time (s)')
	plt.ylabel('Relative Distance (cm)')
	fig2.suptitle(rosbag_parser.foldername + '(fixed solutions only)\ntime vs. relative distance')
	# fig2.savefig('../../../data/' + rosbag_parser.foldername + '/Fixed Distance')

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
fig3.suptitle(rosbag_parser.foldername + '\ntime vs. north east down')
# fig3.savefig('../../../data/' + rosbag_parser.foldername + '/NED')
plt.show()
