from readline import append_history_file
from rosbag_parser import Parser
import numpy as np
import matplotlib.pyplot as plt


baseGpsTopic = '/base/PosVelEcef'
roverRelPosTopic = '/rover/RelPos'
roverGpsTopic = '/rover/PosVelEcef'
baseOdomTopic = '/base_odom'
baseMocapTopic = '/boat_landing_platform_ned'
roverMocapTopic = '/rhodey_ned'
tagTopic = '/tag_detections'
bagfile = '/home/tpool2/apriltag-03.bag'

# parser = Parser(bagfile, baseGpsTopic, roverRelPosTopic, roverGpsTopic, baseOdomTopic, baseMocapTopic, roverMocapTopic, tagTopic)

# parser.parse_and_save()

mocap_data = np.load("apriltag-03_rhodey_ned.npz")
mocap_base_data = np.load("apriltag-03_boat_landing_platform_ned.npz")
odom_data = np.load("apriltag-03_base_odom.npz")

fig = plt.figure()
ax = plt.axes(projection='3d')

true_n = np.array(mocap_data["pn"]) - np.array(mocap_base_data["pn"])
true_e = np.array(mocap_data["pd"]) - np.array(mocap_base_data["pd"])
true_d = np.array(mocap_data["pd"]) - np.array(mocap_base_data["pd"])
# for idx in range(len(mocap_data["pn"])):
#     true_n.append(mocap_data["pn"][idx] - mocap_base_data["pn"][idx] )
#     true_e.append(mocap_data["pe"][idx]  - mocap_base_data["pe"][idx] )
#     true_d.append(mocap_data["pd"][idx]  - mocap_base_data["pd"][idx] )

ax.plot3D(true_n, true_e, true_d)
ax.plot3D(odom_data["pn"], odom_data["pe"], odom_data["pd"])
plt.show()

