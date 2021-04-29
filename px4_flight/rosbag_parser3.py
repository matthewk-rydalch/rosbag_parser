import rosbag
import pickle
from collections import namedtuple
from IPython.core.debugger import set_trace 
import numpy as np
from scipy.spatial.transform import Rotation as R

class Parser:
	def __init__(self,roverOdomTopic,hlcTopic):
		self.roverOdomTopic = roverOdomTopic
		self.hlcTopic = hlcTopic

	def get_rover_odom(self, bag):
		sec = []
		nsec = []
		pn = []
		pe = []
		pd = []

		for topic, msg, t in bag.read_messages(topics=[self.roverOdomTopic]):
				sec.append(t.secs)
				nsec.append(t.nsecs)
				pn.append(msg.pose.pose.position.x)
				pe.append(msg.pose.pose.position.y)
				pd.append(msg.pose.pose.position.z)

		return PosTime(sec,nsec,pn,pe,pd)

	def get_hlc(self, bag):
		sec = []
		nsec = []
		pn = []
		pe = []
		pd = []

		for topic, msg, t in bag.read_messages(topics=[self.hlcTopic]):
				sec.append(t.secs)
				nsec.append(t.nsecs)
				pn.append(msg.pose.pose.position.x)
				pe.append(msg.pose.pose.position.y)
				pd.append(msg.pose.pose.position.z)

		return PosTime(sec,nsec,pn,pe,pd)

class PosTime:
	def __init__(self,sec,nsec,pn,pe,pd):
		self.time = np.array(sec)+np.array(nsec)*1E-9
		self.position = np.array([pn,pe,pd])


