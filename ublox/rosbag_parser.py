#be sure to specify filename in this file
from IPython.core.debugger import set_trace
import rosbag
import pickle
from collections import namedtuple
import numpy as np
from geometry_msgs.msg import Pose

def main():

	#TODO the file name and bag are from a rtk_flight test
	filename = 'error_test1.bag'
	bag = rosbag.Bag('../../../data/ragnarok_tests/' + filename)
	data = Parser()
	relpos = data.get_RelPos(bag)
	bag.close()

	MyStruct = namedtuple("mystruct", "plt")#, plt_virt, drone, hl_cmd, is_flying, is_landing, odom")
	vals = MyStruct(plt)#, plt_virt, drone, hl_cmd, is_flying, is_landing, odom)

	return vals

class Parser:

	def get_PosVelECEF(self, bag):
		sec = []
		nsec = []
		pn = []
		pe = []
		pd = []
		horizontal_accuracy = []
		verticle_accuracy = []
		speed_accuracy = []

		for topic, msg, t in bag.read_messages(topics=['/base/PosVelEcef']):  
			sec.append(msg.header.stamp.secs)
			nsec.append(msg.header.stamp.nsecs)			
			pn.append(msg.position[0])
			pe.append(msg.position[1])
			pd.append(msg.position[2])
			horizontal_accuracy.append(msg.horizontal_accuracy)
			verticle_accuracy.append(msg.vertical_accuracy)
			speed_accuracy.append(msg.speed_accuracy)

		return sec, nsec, pn, pe, pd, horizontal_accuracy, verticle_accuracy, speed_accuracy
        
	def get_PosVelTime(self, bag):
		sec = []
		nsec = []
		flags = []
		numSV = []

		for topic, msg, t in bag.read_messages(topics=['/rover/PosVelTime']):  
			sec.append(msg.header.stamp.secs)
			nsec.append(msg.header.stamp.nsecs)			
			flags.append(msg.flags)
			numSV.append(msg.numSV)

		return sec, nsec, flags, numSV

	def get_RelPos(self, bag):
		sec = []
		nsec = []
		RP_N = []
		RP_E = []
		RP_D = []
		N_hp = []
		E_hp = []
		D_hp = []

		flag = []
		
		for topic, msg, t in bag.read_messages(topics=['/rover/RelPos']):
				
			sec.append(msg.header.stamp.secs)
			nsec.append(msg.header.stamp.nsecs)
			RP_N.append(msg.relPosNED[0])
			RP_E.append(msg.relPosNED[1])
			RP_D.append(msg.relPosNED[2])
			N_hp.append(msg.relPosHPNED[0])
			E_hp.append(msg.relPosHPNED[1])
			D_hp.append(msg.relPosHPNED[2])

			flag.append(msg.flags)

		relpos = [sec, nsec, RP_N, RP_E, RP_D, N_hp, E_hp, D_hp, flag]
		
		return relpos

class pos_orient_time:
	def __init__(self, sec, nsec, x, y, z, orientation):
		self.sec = sec
		self.nsec = nsec
		self.position = [x, y, z]
		self.orientation = orientation

if __name__ == '__main__':
    vals = main()
