from rosbag_parser import Parser
import matplotlib.pyplot as plt
from IPython.core.debugger import set_trace
import rosbag
import numpy as np
import statistics
from collections import namedtuple

def main():

    data = Parser()

    filename = 'error_test2.bag'
    bag = rosbag.Bag('../../../data/' + filename)

    cut_time = False
    start_time = 25
    end_time = 50

    #accuracy_plotter(data, bag)
    #RelPos_plotter(data, bag)
    #SV_fix_plotter(data, bag)
    std_dev_plotter(data, bag)

def std_dev_plotter(data, bag):
    
    sec, nsec, pn, pe, pd, horizontal_accuracy, verticle_accuracy, speed_accuracy = data.get_PosVelECEF(bag)
    bag.close()
    time = np.array(sec)+np.array(nsec)*1E-9

    print_standard_deviation(pn, 'pn standard deviation')
    print_standard_deviation(pe, 'pe standard deviation')
    print_standard_deviation(pd, 'pd standard deviation')

    plt.figure(1)
    plt.plot(time, pn, label = 'ecef_n')
    plt.legend(loc = "upper left")
    plt.figure(2)
    plt.plot(time, pe, label = 'ecef_e')
    plt.legend(loc = "upper left")
    plt.figure(3)
    plt.plot(time, pd, label = 'ecef_d')
    plt.legend(loc = "upper left")

def print_standard_deviation(vals, label):
    
    dif = np.zeros(len(vals))
    i = 0
    xp = vals[0]
    for x in vals:
        dif[i] = x-xp
        xp = x
        i = i+1
    std_dev = statistics.stdev(dif)
    total_std_dev = statistics.stdev(vals)

    print(label, ' = ', std_dev)
    print('total', label, ' = ', total_std_dev)

def RelPos_plotter(data, bag):
    sec, nsec, RP_N, RP_E, RP_D, N_hp, E_hp, D_hp, flag = data.get_RelPos(bag)
    bag.close()

    time = np.array(sec)+np.array(nsec)*1E-9
    rel_pn = np.array(RP_N)+np.array(N_hp)*1E-3
    rel_pe = np.array(RP_E)+np.array(E_hp)*1E-3
    rel_pd = np.array(RP_D)+np.array(D_hp)*1E-3

    title1 = 'rel_pos'
    title2 = 'flags'

    plot_position_2d([rel_pn,rel_pe], title1)
    plt.figure(2)
    plt.plot(time, flag, label=title2)
    plt.legend('upper left')

def SV_fix_plotter(data, bag):
    sec, nsec, flags, numSV = data.get_PosVelTime(bag)
    bag.close()

    time = np.array(sec)+np.array(nsec)*1E-9

    title1 = 'flags'
    title2 = 'numSV'

    fig, axs = plt.subplots(2)
    fig.suptitle('Flags/RoverNumSV')
    axs[0].plot(time, flags, label = title1)
    axs[1].plot(time, numSV, label=title2)

def accuracy_plotter(data,bag):
    acc = data.get_PosVelECEF(bag)
    bag.close()

    title = 'accuracy'

    name = ['horizontal_accuracy', 'verticle_accuracy', 'speed_accuracy']
    plot_accuracy(acc, name, title)

def plot_position_2d(p, title):

    plt.figure(1)
    plt.plot(p[0], p[1], label = title)
    plt.legend(loc = "upper left")

def plot_position_2d_w_hlc(p, hlc, label1, label2):

    plt.figure(1)
    plt.plot(p[0], p[1], label = label1)
    plt.plot(hlc[0],hlc[1], label = label2)
    plt.legend(loc = "upper left")

def plot_accuracy(acc, name, title):

    time = np.array(acc[0])+np.array(acc[1])*1E-9

    plt.plot(time, acc[2], label =  name[0])
    plt.plot(time, acc[3], label = name[1])
    plt.plot(time, acc[4], label = name[2])
    plt.legend(loc = "upper right")

if __name__ == '__main__':
    main()
