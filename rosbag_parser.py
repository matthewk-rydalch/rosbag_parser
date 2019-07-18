#be sure to specify foldername in this file and the true value in rosbag_data.py
from IPython.core.debugger import set_trace

import rosbag

foldername = '125cm_centered_lazy'
bag = rosbag.Bag(foldername + '/data.bag')

relPosNED = []
relPosLength = []
flags = []
secs = []
nsecs = []

print(bag)
for topic, msg, t in bag.read_messages(topics=['/rover/RelPos']):
	#set_trace()
	relPosNED.append(msg.relPosNED)
	relPosLength.append(msg.relPosLength)
	flags.append(msg.flags)
	secs.append(msg.header.stamp.secs)
	nsecs.append(msg.header.stamp.nsecs)


bag.close()