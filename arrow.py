from IPython.core.debugger import set_trace
from importlib import reload
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import rosbag
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set(xlim=(-10,10), ylim=(-10,10), zlim=(-10,10))

bag = rosbag.Bag("/home/magicc/rtk_tests/tworoveronecomp/alldata.bag")

def get_variables(bag, topic, section):
    variable=[]
    for topic, msg, t in bag.read_messages(topics = [topic]):
        variable.append(get_section(msg, section, t))
    #Normalize Time
    if section=='time':
        variable = normalizeTime(variable)
    # print("get_variables variables")
    # print(variable)
    #set_trace()
    return variable

def get_section(msg, section, t=0):
    if section == 'relPosN':
        return msg.relPosNED[0]
    elif section == 'relPosE':
        return msg.relPosNED[1]
    elif section == 'relPosD':
        return msg.relPosNED[2]
    elif section == 'time' or section == 'rosbagtime':
        return [t.secs, t.nsecs]
    elif section == 'Yaw':
        return msg.arrowRPY[2]
    elif section == 'Pitch':
        return msg.arrowRPY[1]
    elif section == 'posN' :
        return msg.position[0]
    else:
        return eval("msg."+section)

#normalizeTime makes the time interval start at zero.
def normalizeTime(times):
    normaltime = []
    for time in times:
        normaltime.append(time[0]-times[0][0]+time[1]*10.00**(-9))

    return normaltime

def init():
    print("Init Function Called")

def updateNED(i, *fargs):
    print("Called updateNED function")
    ax = fargs[1]
    print(NED[i])
    return scattering

NED = get_variables(bag, "/rover/RelPos", "relPosNED")
y = len(NED)
#print(NED)


scattering = [ax.scatter(NED[i][0], NED[i][1], NED[i][2], 'b.') for i in range(y)]

ani = animation.FuncAnimation(fig, updateNED, frames=range(0,y,1), init_func=init, fargs = (fig, ax) , blit=False, interval=1)
print("Why")
plt.draw()
plt.show()