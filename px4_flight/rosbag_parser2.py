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
		qx = []
		qy = []
		qz = []
		qw = []
		vx = []
		vy = []
		vz = []

		for topic, msg, t in bag.read_messages(topics=[self.roverOdomTopic]):
				sec.append(t.secs)
				nsec.append(t.nsecs)
				pn.append(msg.pose.pose.position.x)
				pe.append(msg.pose.pose.position.y)
				pd.append(msg.pose.pose.position.z)
				qx.append(msg.pose.pose.orientation.x)
				qy.append(msg.pose.pose.orientation.y)
				qz.append(msg.pose.pose.orientation.z)
				qw.append(msg.pose.pose.orientation.w)
				vx.append(msg.twist.twist.linear.x)
				vy.append(msg.twist.twist.linear.y)
				vz.append(msg.twist.twist.linear.z)

		return Odom(sec,nsec,pn,pe,pd,qx,qy,qz,qw,vx,vy,vz)

	def get_hlc(self, bag):
		sec = []
		nsec = []
		pn = []
		pe = []
		pd = []
		qx = []
		qy = []
		qz = []
		qw = []
		vx = []
		vy = []
		vz = []

		for topic, msg, t in bag.read_messages(topics=[self.hlcTopic]):
				sec.append(t.secs)
				nsec.append(t.nsecs)
				pn.append(msg.pose.pose.position.x)
				pe.append(msg.pose.pose.position.y)
				pd.append(msg.pose.pose.position.z)
				qx.append(msg.pose.pose.orientation.x)
				qy.append(msg.pose.pose.orientation.y)
				qz.append(msg.pose.pose.orientation.z)
				qw.append(msg.pose.pose.orientation.w)
				vx.append(msg.twist.twist.linear.x)
				vy.append(msg.twist.twist.linear.y)
				vz.append(msg.twist.twist.linear.z)

		return Odom(sec,nsec,pn,pe,pd,qx,qy,qz,qw,vx,vy,vz)

class Odom:
	def __init__(self,sec,nsec,pn,pe,pd,qx,qy,qz,qw,vx,vy,vz):
		self.time = np.array(sec)+np.array(nsec)*1E-9
		# self.time -= self.time[0]
		self.position = np.array([pn,pe,pd])
		quat = np.array([qx,qy,qz,qw]).T
		# eulerRad = R.from_quat(quat).as_euler('xyz').T
		# self.euler = eulerRad*180.0/np.pi
		self.velocity = np.array([vx,vy,vz])


