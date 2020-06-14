from IPython.core.debugger import set_trace
from importlib import reload
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import rosbag
import numpy as np
from scipy import integrate

def main():
    filepath = '/home/magicc/data/multi-rover/2020-05-22-14-36-43.bag'

    bag = rosbag.Bag(filepath)

    rov1_gnssFixOk = []
    rov1_diffSoln = []
    rov1_relPosValid = []
    rov1_CarrSoln = []
    rov1_flags = []
    rov1_isMoving = []
    rov1_refPosMiss = []
    rov1_refObsMiss = []
    rov1_relPosHeadingValid = []
    rov1_relPosNormalized = []
    rov1_RPtime = []
    rov1_PVTtime = []
    rov1_velN = []
    rov1_velE = []
    rov1_velD = []
    rov1_N = []
    rov1_E = []
    rov1_D = []

    rov2_gnssFixOk = []
    rov2_diffSoln = []
    rov2_relPosValid = []
    rov2_CarrSoln = []
    rov2_flags = []
    rov2_isMoving = []
    rov2_refPosMiss = []
    rov2_refObsMiss = []
    rov2_relPosHeadingValid = []
    rov2_relPosNormalized = []
    rov2_RPtime = []
    rov2_PVTtime = []
    rov2_velN = []
    rov2_velE = []
    rov2_velD = []
    rov2_N = []
    rov2_E = []
    rov2_D = []

    for topic, msg, t in bag.read_messages():
        if topic=='/rover1/RelPos':
            rov1_RPtime.append(msg.header.stamp.secs+msg.header.stamp.nsecs*10**-9)
            rov1_N.append(msg.relPosNED[0]+msg.relPosHPNED[0]*10**-9)
            rov1_E.append(msg.relPosNED[1]+msg.relPosHPNED[1]*10**-9)
            rov1_D.append(msg.relPosNED[2]+msg.relPosHPNED[2]*10**-9)
        elif topic=='/rover2/RelPos':
            rov2_RPtime.append(msg.header.stamp.secs+msg.header.stamp.nsecs*10**-9)
            rov2_N.append(msg.relPosNED[0]+msg.relPosHPNED[0]*10**-9)
            rov2_E.append(msg.relPosNED[1]+msg.relPosHPNED[1]*10**-9)
            rov2_D.append(msg.relPosNED[2]+msg.relPosHPNED[2]*10**-9)
        elif topic=='/rover1/PosVelTime':
            rov1_PVTtime.append(msg.header.stamp.secs+msg.header.stamp.nsecs*10**-9)
            rov1_velN.append(msg.velNED[0])
            rov1_velE.append(msg.velNED[1])
            rov1_velD.append(msg.velNED[2])
        elif topic=='/rover2/PosVelTime':
            rov2_PVTtime.append(msg.header.stamp.secs+msg.header.stamp.nsecs*10**-9)
            rov2_velN.append(msg.velNED[0])
            rov2_velE.append(msg.velNED[1])
            rov2_velD.append(msg.velNED[2])
        elif topic=='/rover1/RelPosFlags':
            rov1_gnssFixOk.append(msg.gnssFixOk)
            rov1_diffSoln.append(msg.diffSoln)
            rov1_relPosValid.append(msg.relPosValid)
            rov1_CarrSoln.append(msg.floatCarrSoln+2*msg.fixedCarrSoln)
            rov1_flags.append(msg.flags)
            rov1_isMoving.append(msg.isMoving)
            rov1_refPosMiss.append(msg.refPosMiss)
            rov1_refObsMiss.append(msg.refObsMiss)
            rov1_relPosHeadingValid.append(msg.relPosHeadingValid)
            rov1_relPosNormalized.append(msg.relPosNormalized)
        elif topic=='/rover2/RelPosFlags':
            rov2_gnssFixOk.append(msg.gnssFixOk)
            rov2_diffSoln.append(msg.diffSoln)
            rov2_relPosValid.append(msg.relPosValid)
            rov2_CarrSoln.append(msg.floatCarrSoln+2*msg.fixedCarrSoln)
            rov2_flags.append(msg.flags)
            rov2_isMoving.append(msg.isMoving)
            rov2_refPosMiss.append(msg.refPosMiss)
            rov2_refObsMiss.append(msg.refObsMiss)
            rov2_relPosHeadingValid.append(msg.relPosHeadingValid)
            rov2_relPosNormalized.append(msg.relPosNormalized)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('N')
    ax.set_ylabel('E')
    ax.set_zlabel('D')
    ax.scatter(rov1_N, rov1_E, rov1_D, s=5, c='b', label='Rover 1')
    ax.scatter(rov2_N, rov2_E, rov2_D, s=5, c='g', label = 'Rover 2')
    ax.scatter(0, 0, s=50, c='k', label = 'Base')
    fig.suptitle('Rover 1 and Rover 2')
    ax.legend()
    plt.show()

    fig2, axs2 = plt.subplots(2, 3)

    for row in axs2:
        for ax2 in row:
            ax2.set_xlabel('Time (s)')

    rov1_velN_int = integrate.cumtrapz(rov1_velN, rov1_PVTtime, initial=rov1_N[0]) + rov1_N[0]
    rov1_velE_int = integrate.cumtrapz(rov1_velE, rov1_PVTtime, initial=rov1_E[0]) + rov1_E[0]
    rov1_velD_int = integrate.cumtrapz(rov1_velD, rov1_PVTtime, initial=rov1_D[0]) + rov1_D[0]

    axs2[0,0].scatter(rov1_RPtime, rov1_N, s=5, c='b', label='RelPos')
    axs2[0,0].scatter(rov1_PVTtime, rov1_velN_int, s=5, c='r', label='Vel Int')
    axs2[0,0].legend()
    axs2[0,0].set_title('RelPos N and Integrated Velocity')

    axs2[0,1].scatter(rov1_RPtime, rov1_E, s=5, label='RelPos')
    axs2[0,1].scatter(rov1_PVTtime, rov1_velE_int, s=5, c='r', label='Vel Int')
    axs2[0,1].legend()
    axs2[0,1].set_title('RelPos E and Integrated Velocity')

    axs2[0,2].scatter(rov1_RPtime, rov1_D, s=5, label='RelPos')
    axs2[0,2].scatter(rov1_PVTtime, rov1_velD_int, s=5, c='r', label='Vel Int')
    axs2[0,2].legend()
    axs2[0,2].set_title('RelPos D and Integrated Velocity')

    axs2[1,0].scatter(rov1_PVTtime, rov1_velN, s=5, c='r')
    axs2[1,0].set_title('Vel N', loc='left')
    axs2[1,1].scatter(rov1_PVTtime, rov1_velE, s=5, c='r')
    axs2[1,1].set_title('Vel E', loc='left')
    axs2[1,2].scatter(rov1_PVTtime, rov1_velD, s=5, c='r')
    axs2[1,2].set_title('Vel D', loc='left')
    fig2.suptitle('Rover 1')
    plt.tight_layout

    fig3, axs3 = plt.subplots(2, 3)

    for row in axs3:
        for ax3 in row:
            ax3.set_xlabel('Time (s)')

    rov2_velN_int = integrate.cumtrapz(rov2_velN, rov2_PVTtime, initial=rov2_N[0]) + rov2_N[0]
    rov2_velE_int = integrate.cumtrapz(rov2_velE, rov2_PVTtime, initial=rov2_E[0]) + rov2_E[0]
    rov2_velD_int = integrate.cumtrapz(rov2_velD, rov2_PVTtime, initial=rov2_D[0]) + rov2_D[0]

    axs3[0,0].scatter(rov2_RPtime, rov2_N, s=5, c='b', label='RelPos')
    axs3[0,0].scatter(rov2_PVTtime, rov2_velN_int, s=5, c='r', label='Vel Int')
    axs3[0,0].legend()
    axs3[0,0].set_title('RelPos N and Integrated Velocity')

    axs3[0,1].scatter(rov2_RPtime, rov2_E, s=5, label='RelPos')
    axs3[0,1].scatter(rov2_PVTtime, rov2_velE_int, s=5, c='r', label='Vel Int')
    axs3[0,1].legend()
    axs3[0,1].set_title('RelPos E and Integrated Velocity')

    axs3[0,2].scatter(rov2_RPtime, rov2_D, s=5, label='RelPos')
    axs3[0,2].scatter(rov2_PVTtime, rov2_velD_int, s=5, c='r', label='Vel Int')
    axs3[0,2].legend()
    axs3[0,2].set_title('RelPos D and Integrated Velocity')

    axs3[1,0].scatter(rov2_PVTtime, rov2_velN, s=5, c='r')
    axs3[1,0].set_title('Vel N', loc='left')
    axs3[1,1].scatter(rov2_PVTtime, rov2_velE, s=5, c='r')
    axs3[1,1].set_title('Vel E', loc='left')
    axs3[1,2].scatter(rov2_PVTtime, rov2_velD, s=5, c='r')
    axs3[1,2].set_title('Vel D', loc='left')
    fig3.suptitle('Rover 2')
    plt.tight_layout

    fig4, axs4 = plt.subplots(2, 5)

    for row in axs4:
        for ax4 in row:
            ax4.set_xlabel('Time (s)')
            ax4.set_ylim(-.25, 1.25)

    axs4[0,0].scatter(rov1_RPtime, rov1_gnssFixOk, s=5)
    axs4[0,0].set_title('gnssFixOk')

    axs4[0,1].scatter(rov1_RPtime, rov1_diffSoln, s=5)
    axs4[0,1].set_title('diffSoln')

    axs4[0,2].scatter(rov1_RPtime, rov1_relPosValid, s=5)
    axs4[0,2].set_title('relPosValid')

    axs4[0,3].scatter(rov1_RPtime, rov1_CarrSoln, s=5)
    axs4[0,3].set_ylim(0, 2.5)
    axs4[0,3].set_title('CarrSoln')

    axs4[0,4].scatter(rov1_RPtime, rov1_flags, s=5)
    axs4[0,4].set_ylim(0, 400)
    axs4[0,4].set_title('Flags')

    axs4[1,0].scatter(rov1_RPtime, rov1_isMoving, s=5)
    axs4[1,0].set_title('isMoving')

    axs4[1,1].scatter(rov1_RPtime, rov1_refPosMiss, s=5)
    axs4[1,1].set_title('refPosMiss')
    
    axs4[1,2].scatter(rov1_RPtime, rov1_refObsMiss, s=5)
    axs4[1,2].set_title('refObsMiss')
    
    axs4[1,3].scatter(rov1_RPtime, rov1_relPosHeadingValid, s=5)
    axs4[1,3].set_title('relPosHeadingValid')
    
    axs4[1,4].scatter(rov1_RPtime, rov1_relPosNormalized, s=5)
    axs4[1,4].set_title('relPosNormalized')

    fig4.suptitle('Rover 1 RelPosFlags')

    fig5, axs5 = plt.subplots(2, 5)

    for row in axs5:
        for ax5 in row:
            ax5.set_xlabel('Time (s)')
            ax5.set_ylim(-.25, 1.25)

    axs5[0,0].scatter(rov2_RPtime, rov2_gnssFixOk, s=5)
    axs5[0,0].set_title('gnssFixOk')

    axs5[0,1].scatter(rov2_RPtime, rov2_diffSoln, s=5)
    axs5[0,1].set_title('diffSoln')

    axs5[0,2].scatter(rov2_RPtime, rov2_relPosValid, s=5)
    axs5[0,2].set_title('relPosValid')

    axs5[0,3].scatter(rov2_RPtime, rov2_CarrSoln, s=5)
    axs5[0,3].set_ylim(0, 2.5)
    axs5[0,3].set_title('CarrSoln')

    axs5[0,4].scatter(rov2_RPtime, rov2_flags, s=5)
    axs5[0,4].set_ylim(0, 400)
    axs5[0,4].set_title('Flags')

    axs5[1,0].scatter(rov2_RPtime, rov2_isMoving, s=5)
    axs5[1,0].set_title('isMoving')

    axs5[1,1].scatter(rov2_RPtime, rov2_refPosMiss, s=5)
    axs5[1,1].set_title('refPosMiss')
    
    axs5[1,2].scatter(rov2_RPtime, rov2_refObsMiss, s=5)
    axs5[1,2].set_title('refObsMiss')
    
    axs5[1,3].scatter(rov2_RPtime, rov2_relPosHeadingValid, s=5)
    axs5[1,3].set_title('relPosHeadingValid')
    
    axs5[1,4].scatter(rov2_RPtime, rov2_relPosNormalized, s=5)
    axs5[1,4].set_title('relPosNormalized')

    fig5.suptitle('Rover 2 RelPosFlags')

    plt.show()

if __name__ == "__main__":
    main()


#Groot was rover 1 and the the laptop was rover 2. It would appear
# having no obstructions on the same height makes a large difference
