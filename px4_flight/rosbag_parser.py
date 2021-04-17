import rosbag
import pickle
from collections import namedtuple
import numpy as np
from scipy.spatial.transform import Rotation as R

class Parser:
	def __init__(self,flightModeTopic,missionStateTopic,baseGpsTopic,baseImuTopic,roverRelPosTopic):
		self.flightModeTopic = flightModeTopic
		self.missionStateTopic = missionStateTopic
		self.baseGpsTopic = baseGpsTopic
		self.baseImuTopic = baseImuTopic
		self.roverRelPosTopic = roverRelPosTopic

	def get_flight_mode(self, bag):
		sec = []
		nsec = []
		flightMode = []

		for topic, msg, t in bag.read_messages(topics=[self.flightModeTopic]):
			sec.append(msg.header.stamp.secs)
			nsec.append(msg.header.stamp.nsecs)
			flightMode.append(msg.point.x)

		return FlightMode(sec,nsec,flightMode)

	def get_mission_state(self, bag):
		sec = []
		nsec = []
		missionState = []

		for topic, msg, t in bag.read_messages(topics=[self.missionStateTopic]):
			sec.append(msg.header.stamp.secs)
			nsec.append(msg.header.stamp.nsecs)
			missionState.append(msg.point.x)

		return MissionState(sec,nsec,missionState)

	def get_base_gps(self, bag):
		sec = []
		nsec = []
		px = []
		py = []
		pz = []
		vx = []
		vy = []
		vz = []

		for topic, msg, t in bag.read_messages(topics=[self.baseGpsTopic]):
			sec.append(msg.header.stamp.secs)
			nsec.append(msg.header.stamp.nsecs)
			px.append(msg.position[0])
			py.append(msg.position[1])
			pz.append(msg.position[2])
			vx.append(msg.velocity[0])
			vy.append(msg.velocity[1])
			vz.append(msg.velocity[2])

		return Gps(sec,nsec,px,py,pz,vx,vy,vz)

	def get_imu(self, bag):
		sec = []
		nsec = []
		ax = []
		ay = []
		az = []
		wx = []
		wy = []
		wz = []

		for topic, msg, t in bag.read_messages(topics=[self.baseImuTopic]):
			sec.append(msg.header.stamp.secs)
			nsec.append(msg.header.stamp.nsecs)
			ax.append(msg.linear_acceleration.x)
			ay.append(msg.linear_acceleration.y)
			az.append(msg.linear_acceleration.z)
			wx.append(msg.angular_velocity.x)
			wy.append(msg.angular_velocity.y)
			wz.append(msg.angular_velocity.z)

		return Imu(sec,nsec,ax,ay,az,wx,wy,wz)

	def get_rover_relPos(self, bag):
		sec = []
		nsec = []
		pn = []
		pe = []
		pd = []
		pnHp = []
		peHp = []
		pdHp = []

		for topic, msg, t in bag.read_messages(topics=[self.roverRelPosTopic]):
			sec.append(msg.header.stamp.secs)
			nsec.append(msg.header.stamp.nsecs)
			pn.append(msg.relPosNED[0])
			pe.append(msg.relPosNED[1])
			pd.append(msg.relPosNED[2])
			pnHp.append(msg.relPosHPNED[0])
			peHp.append(msg.relPosHPNED[1])
			pdHp.append(msg.relPosHPNED[2])

		return RelPos(sec,nsec,pn,pe,pd,pnHp,peHp,pdHp)

class FlightMode:
	def __init__(self,sec,nsec,flightMode):
		self.time = np.array(sec)+np.array(nsec)*1E-9
		self.flightMode = flightMode

class MissionState:
	def __init__(self,sec,nsec,missionState):
		self.time = np.array(sec)+np.array(nsec)*1E-9
		self.missionState = missionState

class Gps:
	def __init__(self,sec,nsec,px,py,pz,vx,vy,vz):
		self.time = np.array(sec)+np.array(nsec)*1E-9
		# self.time -= self.time[0]
		self.position = np.array([px,py,pz])
		self.velocity = np.array([vx,vy,vz])

class Imu:
	def __init__(self,sec,nsec,ax,ay,az,wx,wy,wz):
		self.time = np.array(sec)+np.array(nsec)*1E-9
		# self.time -= self.time[0]
		self.accel = np.array([ax,ay,az])
		self.omega = np.array([wx,wy,wz])

class RelPos:
	def __init__(self,sec,nsec,pn,pe,pd,pnHp=0.0,peHp=0.0,pdHp=0.0):
		self.time = np.array(sec)+np.array(nsec)*1E-9
		# self.time -= self.time[0]
		pn = np.array(pn) + np.array(pnHp)
		pe = np.array(pe) + np.array(peHp)
		pd = np.array(pd) + np.array(pdHp)
		self.position = np.array([pn,pe,pd])
