from IPython.core.debugger import set_trace
import rosbag
import rospy
import pickle
from collections import namedtuple
import numpy as np
import sys
import matplotlib.pyplot as plt

def main():
    filename = sys.argv[1]
    print(filename)

    if(sys.argv[2]=='PVT'):
        topic1 = '/base/PosVelTime'
        topic2 = '/rover/base/PosVelTime'
    elif(sys.argv[2]=='ECEF'):
        topic1 = '/base/PosVelEcef'
        topic2 = '/rover/base/PosVelEcef'


    bag = rosbag.Bag(filename)

    ecef_fig, ecef_axs = plt.subplots(2,3)

    ecef_fig.suptitle("Base "+sys.argv[2])

    base_time_ = []
    base_true_x_ = []
    base_true_y_ = []
    base_true_z_ = []
    base_true_vel_x_ = []
    base_true_vel_y_ = []
    base_true_vel_z_ = []

    rover_time_ = []
    base_sent_x_ = []
    base_sent_y_ = []
    base_sent_z_ = []
    base_sent_vel_x_ = []
    base_sent_vel_y_ = []
    base_sent_vel_z_ = []

    rover_ecef_time_ = []
    rover_ecef_x_ = []
    rover_ecef_vel_x_ = []


    for topic, msg, t in bag.read_messages(topics=[topic1, topic2, '/rover/PosVelEcef']):
        if(topic==topic1):
            base_time_.append(t.secs + (t.nsecs)*10**-9 -bag.get_start_time())
            if(sys.argv[2]=='ECEF'):
                base_true_x_.append(msg.position[0])
                base_true_y_.append(msg.position[1])
                base_true_z_.append(msg.position[2])
                base_true_vel_x_.append(msg.velocity[0])
                base_true_vel_y_.append(msg.velocity[1])
                base_true_vel_z_.append(msg.velocity[2])
            elif(sys.argv[2]=='PVT'):
                base_true_x_.append(msg.lla[0])
                base_true_y_.append(msg.lla[1])
                base_true_z_.append(msg.lla[2])
                base_true_vel_x_.append(msg.velNED[0])
                base_true_vel_y_.append(msg.velNED[1])
                base_true_vel_z_.append(msg.velNED[2])

        elif(topic==topic2):
            rover_time_.append(t.secs + (t.nsecs)*10**-9 -bag.get_start_time())
            if(sys.argv[2]=='ECEF'):
                base_sent_x_.append(msg.position[0])
                base_sent_y_.append(msg.position[1])
                base_sent_z_.append(msg.position[2])
                base_sent_vel_x_.append(msg.velocity[0])
                base_sent_vel_y_.append(msg.velocity[1])
                base_sent_vel_z_.append(msg.velocity[2])
            elif(sys.argv[2]=='PVT'):
                base_sent_x_.append(msg.lla[0])
                base_sent_y_.append(msg.lla[1])
                base_sent_z_.append(msg.lla[2])
                base_sent_vel_x_.append(msg.velNED[0])
                base_sent_vel_y_.append(msg.velNED[1])
                base_sent_vel_z_.append(msg.velNED[2])
                
        elif(topic=='/rover/PosVelEcef'):
            rover_ecef_time_.append(t.secs + (t.nsecs)*10**-9 -bag.get_start_time())
            rover_ecef_x_.append(msg.position[0])
            rover_ecef_vel_x_.append(msg.velocity[0])

    ecef_axs[0,0].set_title(sys.argv[2] + " Position X")
    ecef_axs[0,0].plot(base_time_, base_true_x_, label='On Base')
    ecef_axs[0,0].scatter(rover_time_, base_sent_x_, s=4, c='r', marker='o', label='On Rover')
    # ecef_axs[0,0].scatter(rover_ecef_time_, rover_ecef_x_, s=4, c='g', marker='+', label='Rover Ecef')
    ecef_axs[0,0].legend()

    ecef_axs[0,1].set_title(sys.argv[2] + " Position Y")
    ecef_axs[0,1].plot(base_time_, base_true_y_, label='On Base')
    ecef_axs[0,1].scatter(rover_time_, base_sent_y_, s=4, c='r', marker='o', label='On Rover')
    ecef_axs[0,1].legend()

    ecef_axs[0,2].set_title(sys.argv[2] + " Position Z")
    ecef_axs[0,2].plot(base_time_, base_true_z_, label='On Base')
    ecef_axs[0,2].scatter(rover_time_, base_sent_z_, s=4, c='r', marker='o', label='On Rover')
    ecef_axs[0,2].legend()

    ecef_axs[1,0].set_title(sys.argv[2] + " Velocity X")
    ecef_axs[1,0].scatter(base_time_, base_true_vel_x_, label='On Base')
    ecef_axs[1,0].scatter(rover_time_, base_sent_vel_x_, s=4, c='r', marker='o', label='On Rover')
    # ecef_axs[1,0].scatter(rover_ecef_time_, rover_ecef_vel_x_, s=4, c='g', marker='+', label='Rover Ecef')
    ecef_axs[1,0].legend()

    ecef_axs[1,1].set_title(sys.argv[2] + " Velocity Y")
    ecef_axs[1,1].scatter(base_time_, base_true_vel_y_, label='On Base')
    ecef_axs[1,1].scatter(rover_time_, base_sent_vel_y_, s=4, c='r', marker='o', label='On Rover')
    ecef_axs[1,1].legend()

    ecef_axs[1,2].set_title(sys.argv[2] + " Velocity Z")
    ecef_axs[1,2].scatter(base_time_, base_true_vel_z_, label='On Base')
    ecef_axs[1,2].scatter(rover_time_, base_sent_vel_z_, s=4, c='r', marker='o', label='On Rover')
    ecef_axs[1,2].legend()

    for row in ecef_axs:
        for ax in row:
            ax.set_xlabel('Time (s)')





if __name__ == "__main__":
    main()
    plt.show()