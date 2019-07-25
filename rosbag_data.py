from IPython.core.debugger import set_trace
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np
import rosbag_parser

def twos_complement(val):
	if val > 21474836.48:
		Dec = round(val*100) #in cm
		print(Dec)
		bit = [0]*32
		j = 31
		Dec = Dec-1
		new_val = 0
		for i in range(0,31):
			if Dec >= 2**j:
				bit[i] = 0
				Dec = Dec - 2**j
			else:
				bit[i] = 1
			new_val = new_val + bit[i]*2**j
			j = j-1
		new_val = -new_val
		print(new_val)


	print(bit)


reload(rosbag_parser)

nsecs = np.array([i*1E-9 for i in rosbag_parser.nsecs])
secs = np.array(rosbag_parser.secs)
flags = rosbag_parser.flags
relPosLength = np.array(rosbag_parser.relPosLength)
###############remove mulitplier now that it is fixed in ublox_ros.cpp###################3
relPosHPLength = np.array(rosbag_parser.relPosHPLength)*10
Length = relPosLength+relPosHPLength

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
time = secs+nsecs-secs[0]-nsecs[0]
size = len(time)
lat = []
lon = []
alt = []
for i in range(0,size-1):
	lat.append(rosbag_parser.lla[i][0])
	lon.append(rosbag_parser.lla[i][1])
	alt.append(rosbag_parser.lla[i][2])

for i in range(0,size):
	twos_complement(rosbag_parser.relPosNED[i][0])
	north.append(rosbag_parser.relPosNED[i][0])
	east.append(rosbag_parser.relPosNED[i][1])
	down.append(rosbag_parser.relPosNED[i][2])
	northHP.append(rosbag_parser.relPosNEDHP[i][0])
	eastHP.append(rosbag_parser.relPosNEDHP[i][1])
	downHP.append(rosbag_parser.relPosNEDHP[i][2])
	North.append(north[i]+northHP[i])
	East.append(east[i]+eastHP[i])
	Down.append(down[i]+downHP[i])

fix_time = []
fix_dis = []
float_time = []
float_dis = []

True_value = 2.50
Truth = [size]
Truth = [True_value]*size

for i in range(0,size):
	if flags[i] == 375 or flags[i] == 179 or flags[i] == 311 or flags[i] == 243 or flags[i] == 279:
		fix_time.append(time[i])
		fix_dis.append(Length[i])
	else:
		float_time.append(time[i])
		float_dis.append(Length[i])

#find time to fix
time_to_fix = fix_time[0]

#find average fixed length
fix_len = len(fix_dis)
average_length = 100*sum(fix_dis)/fix_len #in cm

#find average fixed maginitude error
error = [abs(x-True_value) for x in fix_dis]
average_error = 100*sum(error)/fix_len #in cm

fig = plt.figure()
plt.plot(time, Truth, color = "black", label ="Truth")
plt.scatter(fix_time, fix_dis, s=1, color="red", label="fixed lengths")
plt.scatter(float_time, float_dis, s=1, color="blue", label="float lengths")
plt.legend(loc='upper right', prop={'size': 16}, frameon=False)
plt.xlabel('time (s)')
plt.ylabel('Relative Distance (m)')
#plt.figtext(.8, .5, 'Time to Fix = %d \n Average Length = %d' % (time_to_fix, average_length))
plt.figtext(.5, .5, 'Time to Fix = %f s \nAverage Length = %f cm \nAverage Error = %f cm' % (time_to_fix, average_length, average_error))
fig.suptitle(rosbag_parser.foldername + '_susan_test\ntime vs. relative distance')
fig.savefig('../../../data/' + rosbag_parser.foldername + '/Relative Distance')

Truth_cm = [i*100 for i in Truth]
fix_dis_cm = [i*100 for i in fix_dis]
fig2 = plt.figure()
plt.plot(time, Truth_cm, color = "black", label ="Truth")
plt.scatter(fix_time, fix_dis_cm, s=1, color="red", label="fixed lengths")
plt.legend(loc='upper left', prop={'size': 16}, frameon=False)
plt.xlabel('time (s)')
plt.ylabel('Relative Distance (cm)')
fig2.suptitle(rosbag_parser.foldername + '_susan_test (fixed solutions only)\ntime vs. relative distance')
fig2.savefig('../../../data/' + rosbag_parser.foldername + '/Relative Distance Fixed Only')

plt.plot(time, North, color="red", label="North")
plt.plot(time, East, color="blue", label="East")
plt.plot(time, Down, color="green", label="Down")
plt.legend(loc='upper right', prop={'size': 16}, frameon=False)
plt.xlabel('time (s)')
plt.ylabel('Relative Distance (m)')
#plt.figtext(.8, .5, 'Time to Fix = %d \n Average Length = %d' % (time_to_fix, average_length))
plt.figtext(.5, .5, 'Time to Fix = %f s \nAverage Length = %f cm \nAverage Error = %f cm' % (time_to_fix, average_length, average_error))
fig.suptitle(rosbag_parser.foldername + '_susan_test\ntime vs. relative distance')
plt.show()
