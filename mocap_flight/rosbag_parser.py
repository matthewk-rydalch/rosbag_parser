import rosbag
import pickle
from collections import namedtuple
import numpy as np
from scipy.spatial.transform import Rotation as R

class Parser:
	def __init__(self,mocapTopic,baseEulerTopic):
		self.mocapTopic = mocapTopic
		self.baseEulerTopic = baseEulerTopic

	def get_mocap(self, bag):
		sec = []
		nsec = []
		qx = []
		qy = []
		qz = []
		qw = []

		for topic, msg, t in bag.read_messages(topics=[self.mocapTopic]):
				sec.append(t.secs)
				nsec.append(t.nsecs)
				qx.append(msg.pose.orientation.x)
				qy.append(msg.pose.orientation.y)
				qz.append(msg.pose.orientation.z)
				qw.append(msg.pose.orientation.w)
		return Quat(sec,nsec,qx,qy,qz,qw)

	def get_base_euler(self, bag):
		sec = []
		nsec = []
		phi = []
		theta = []
		psi = []

		for topic, msg, t in bag.read_messages(topics=[self.baseEulerTopic]):
				sec.append(t.secs)
				nsec.append(t.nsecs)
				phi.append(msg.vector.x)
				theta.append(msg.vector.y)
				psi.append(msg.vector.z)

		return Euler(sec,nsec,phi,theta,psi)


class Quat:
	def __init__(self,sec,nsec,qx,qy,qz,qw):
		self.time = np.array(sec)+np.array(nsec)*1E-9
		self.quat = [qx,qy,qz,qw]

class Euler:
	def __init__(self,sec,nsec,phi,theta,psi):
		self.time = np.array(sec)+np.array(nsec)*1E-9
		self.euler = [phi,theta,psi]

