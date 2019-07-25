#be sure to specify foldername in this file
from IPython.core.debugger import set_trace

import rosbag

foldername = 'redo_rod/one'
bag = rosbag.Bag('../../../data/' + foldername + '/data2.bag')
relPosNED = []
relPosNEDHP = []
relPosLength = []
relPosHPLength = []
flags = []
secs = []
nsecs = []
lla = []

for topic, msg, t in bag.read_messages(topics=['/rover/RelPos']):
	relPosNED.append(msg.relPosNED)
	relPosNEDHP.append(msg.relPosHPNED)
	relPosLength.append(msg.relPosLength)
	relPosHPLength.append(msg.relPosHPLength)	
	flags.append(msg.flags)
	secs.append(msg.header.stamp.secs)
	nsecs.append(msg.header.stamp.nsecs)

for topic, msg, t in bag.read_messages(topics=['/rover/PosVelTime']):
	lla.append(msg.lla)

bag.close()