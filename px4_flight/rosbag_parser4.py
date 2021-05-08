import rosbag
import pickle
from collections import namedtuple
from IPython.core.debugger import set_trace 
import numpy as np
from scipy.spatial.transform import Rotation as R

class Parser:
	def __init__(self,roverOdomTopic,hlcTopic,boatOdomTopic,missionStateTopic,flightModeTopic):
		self.roverOdomTopic = roverOdomTopic
		self.hlcTopic = hlcTopic
		self.boatOdomTopic = boatOdomTopic
		self.missionStateTopic = missionStateTopic
		self.flightModeTopic = flightModeTopic

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

	def get_boat_odom(self, bag):
		sec = []
		nsec = []
		pn = []
		pe = []
		pd = []

		for topic, msg, t in bag.read_messages(topics=[self.boatOdomTopic]):
				sec.append(t.secs)
				nsec.append(t.nsecs)
				pn.append(msg.pose.pose.position.x)
				pe.append(msg.pose.pose.position.y)
				pd.append(msg.pose.pose.position.z)

		return PosTime(sec,nsec,pn,pe,pd)

	def get_mission_state(self, bag):
		sec = []
		nsec = []
		state = []

		for topic, msg, t in bag.read_messages(topics=[self.missionStateTopic]):
				sec.append(t.secs)
				nsec.append(t.nsecs)
				state.append(msg.point.x)

		return ValTime(sec,nsec,state)

	def get_flight_mode(self, bag):
		sec = []
		nsec = []
		mode = []

		for topic, msg, t in bag.read_messages(topics=[self.flightModeTopic]):
				sec.append(t.secs)
				nsec.append(t.nsecs)
				mode.append(msg.point.x)

		return ValTime(sec,nsec,mode)

class PosTime:
	def __init__(self,sec,nsec,pn,pe,pd):
		self.time = np.array(sec)+np.array(nsec)*1E-9
		self.position = np.array([pn,pe,pd])

class ValTime:
	def __init__(self,sec,nsec,val):
		self.time = np.array(sec)+np.array(nsec)*1E-9
		self.val = val

