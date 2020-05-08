from IPython.core.debugger import set_trace
from importlib import reload
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import rosbag
import numpy as np
import xml.etree.ElementTree as ET
import math
import parserplot

fig, axs = plt.subplots(3,2)

bagnames = []
bagnames.append(['/home/magicc/Downloads/rover_moving_laptop.bag', 'moving', 'Laptop Moving'])
bagnames.append(['/home/magicc/Downloads/rover_moving_tx2.bag', 'stationary', 'TX2 Moving'])
bagnames.append(['/home/magicc/Downloads/rover_stationary_laptop.bag', 'stationary', 'Laptop Stationary'])
bagnames.append(['/home/magicc/Downloads/rover_stationary_tx2.bag', 'stationary', 'TX2 Stationary'])
bagnames.append(['/home/magicc/Downloads/taylor_onebase.bag', 'stationary', 'Odroid'])
bagnames.append(['/home/magicc/Downloads/taylor_onecomp.bag', 'stationary', 'Odroid'])

i=0
for name in bagnames:
    bag = rosbag.Bag(name[0])
    times = parserplot.get_variables(bag, '/rover/RelPos', 'time')
    flags = parserplot.get_variables(bag, '/rover/RelPos', 'flags')
    
    colors = []
    for flag in flags:
        colors.append('g') if (flag==279 and name[1]=='stationary') or (flag==311 and name[1]=='moving') else colors.append('r')
    
    ax = axs[0 if i==0 else int(math.log2(i)), i%2]
    ax.set_xlabel('Time (sec)', fontdict={'fontsize': 8})
    ax.set_ylabel('Flags', fontdict={'fontsize': 8})
    ax.set_title(name[2], fontdict={'fontsize': 8})
    ax.scatter(times, flags, s=5, c=colors, marker=',')
    i+=1



plt.show()