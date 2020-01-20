from IPython.core.debugger import set_trace
from importlib import reload
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import rosbag
import numpy as np
import xml.etree.ElementTree as ET

def main():
    tree = loadXML(sys.argv[1])  #Load from the XML file and return a tree
    parseXML(tree)

def loadXML(filename='params/secondtest.xml'):
    tree = ET.parse(filename)
    return tree

def parseXML(tree):
    for figure in tree:
        fig = plt.figure()
        for axes in figure:
            if axes.get('type') == "3d":
                ax = fig.add_subplot(projection='3d')
                for plot_type in axes:
                    rosplot(ax ,plot_type)
            elif axis.get('type') == '2d':
                ax=fig.add_subplot()

    for file in files:
        bag = rosbag.Bag(file.findtext('path')+file.findtext('name'))
        fileitr = file.iter()

        for element in fileitr:
            if element.tag =='figure' or element.tag == 'plot':
                rosplot(bag, element)

def rosplot(bag, plot):

    variables = []
    axistitles = []
    title = plot.get('title')

    for plot_type in plot:

        for axis in plot_type:
            variables.append(get_variables(bag, axis.findtext('topic'), axis.findtext('section')))
            axistitles.append(axis.findtext('topic')+"/"+axis.findtext('section'))

        if(len(variables)==2):
            #print("2D")
            plot_2d(variables, axistitles, title, plot_type.tag)

        elif(len(variables)==3):
            #print("3D")
            plot_3d(variables, axistitles, title, plot_type.tag)
        else:
            print("Error: Too many axis")

#470 tanner 3:30

def plot_3d(variables, axistitles, title, plot_type = 'scatter'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel(axistitles[0])
    ax.set_ylabel(axistitles[1])
    ax.set_zlabel(axistitles[2])
    ax.set_title(title)
    eval('ax.'+plot_type+"(variables[0], variables[1], variables[2])")
    plt.show()

def plot_2d(variables, axistitles = ['Axis 1', 'Axis 2'], title = 'No Title', plot_type = 'scatter'):
    plt.xlabel(axistitles[0])
    plt.ylabel(axistitles[1])
    plt.suptitle(title)
    plt.plot(variables[0], variables[1])
    #eval('plt.'+plot_type+'(variables[0], variables[1])')
    #for x in variables[0]:
    #    print(x)
    plt.show()

def get_variables(bag, topic, section):
    variable=[]
    for topic, msg, t in bag.read_messages(topics = [topic]):
        variable.append(get_section(msg, section, t))
    #Normalize Time
    if section=='time':
        variable = normalizeTime(variable)
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
    else:
        return eval("msg."+section)

#normalizeTime makes the time interval start at zero.
def normalizeTime(times):
    normaltime = []
    for time in times:
        normaltime.append(time[0]-times[0][0]+time[1]*10.00**(-9))

    return normaltime

#Run the main function
if __name__=="__main__":
    main()