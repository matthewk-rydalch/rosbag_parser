from IPython.core.debugger import set_trace
from importlib import reload
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import namedtuple
import matplotlib.animation as animation
import sys
import rosbag
import numpy as np
import xml.etree.ElementTree as ET
import statistics as stat
import gmplot
import WaypointConvert as wc

def main():
    #tree = loadXML(sys.argv[1])  #Load from the XML file and return a tree
    #struct = parseXML(tree)

    #print(len(struct.variable))

    bag = rosbag.Bag('/home/magicc/rtk_tests/gnssvsrtk/mar03_2020nomvtbag/mar03_2020nomvtbag.bag')

    lat = get_variables(bag, '/base/PosVelTime', 'lat')
    longitude = get_variables(bag, '/base/PosVelTime', 'long')
    alt = get_variables(bag, '/base/PosVelTime', 'alt')
    time = get_variables(bag, '/base/PosVelTime', 'time')
    base_horiz_acc = get_variables(bag, '/base/PosVelTime', 'hAcc')

    rover_latitude = get_variables(bag, '/rover/PosVelTime', 'lat')
    rover_longitude = get_variables(bag, '/rover/PosVelTime', 'long')
    rover_altitude = get_variables(bag, '/rover/PosVelTime', 'alt')
    rover_time = get_variables(bag, '/rover/PosVelTime', 'time')

    rover_posveltime = get_variables(bag, '/rover/PosVelTime', '')
    base_posveltime = get_variables(bag, '/base/PosVelTime', '')

    relPosGPSTime = []
    relPosGPS = []
    relPosGPSN = []
    relPosGPSE = []
    relPosGPSD = []

    base_start = 0
    rover_start_time = rover_posveltime[0].header.stamp.secs+rover_posveltime[0].header.stamp.nsecs*10**(-9)

    for msg in rover_posveltime:
        rover_timestamp = msg.header.stamp.secs+msg.header.stamp.nsecs*10**(-9)

        for base_index in range(base_start, len(base_posveltime)):
            base_msg = base_posveltime[base_index]
            base_timestamp = base_msg.header.stamp.secs+base_msg.header.stamp.nsecs*10**(-9)

            if(base_timestamp>= rover_timestamp and base_index!=0 and rover_timestamp-rover_start_time>=5):
                relPosGPSTime.append(rover_timestamp-rover_start_time)
                relPosGPS_stamp = wc.to_meters(base_msg.lla[0], base_msg.lla[1], base_msg.lla[2], msg.lla[0], msg.lla[1], msg.lla[2], 0)
                relPosGPS.append(wc.to_meters(base_msg.lla[0], base_msg.lla[1], base_msg.lla[2], msg.lla[0], msg.lla[1], msg.lla[2], 0))
                relPosGPSN.append(relPosGPS_stamp[0])
                relPosGPSE.append(relPosGPS_stamp[1])
                base_start=base_index
                break
    

    print(relPosGPS[0])
    print(relPosGPSTime[0])

    fig_gps_time_north = plt.figure()
    fig_gps_time_north.suptitle('Relative North Position: Conventional GPS')
    plt.xlabel('Time (s)')
    plt.ylabel('GPS Relative North Position (m)')
    plt.scatter(relPosGPSTime, relPosGPSN)
    plt.plot(time, [stat.mean(relPosGPSN)]*len(time), 'r--', label = 'Mean Average: %.3f m' %stat.mean(relPosGPSN))
    plt.plot(time, [stat.mean(relPosGPSN)-stat.stdev(relPosGPSN)]*len(time), 'g--', label = 'Standard Deviation: %.5f m' %stat.stdev(relPosGPSN))
    plt.plot(time, [stat.mean(relPosGPSN)+stat.stdev(relPosGPSN)]*len(time), 'g--')
    plt.legend()

    fig_gps_time_east = plt.figure()
    fig_gps_time_east.suptitle('Relative East Position: Conventional GPS')
    plt.xlabel('Time (s)')
    plt.ylabel('GPS Relative East Position (m)')
    plt.scatter(relPosGPSTime, relPosGPSE)
    plt.plot(time, [stat.mean(relPosGPSE)]*len(time), 'r--', label = 'Mean Average: %.3f m' %stat.mean(relPosGPSE))
    plt.plot(time, [stat.mean(relPosGPSE)-stat.stdev(relPosGPSE)]*len(time), 'g--', label = 'Standard Deviation: %.5f m' %stat.stdev(relPosGPSE))
    plt.plot(time, [stat.mean(relPosGPSE)+stat.stdev(relPosGPSE)]*len(time), 'g--')
    plt.legend()



    print('Base Latitude Length: %f' %len(lat))
    print(len(longitude))
    print(len(alt))
    print(len(time))
    print('Rover Latitude Length: %f' %len(rover_latitude))

    figtimelat = plt.figure()
    figtimelat.suptitle('Base Latitude vs Time')
    plt.axis([0, time[len(time)-1], stat.mean(lat)-2*stat.stdev(lat),stat.mean(lat)+3*stat.stdev(lat)])
    plt.xlabel('Time (s)')
    plt.ylabel('Latitude (Degrees)')
    plt.scatter(time, lat)
    plt.plot(time, [stat.mean(lat)]*len(time), 'r--', label = 'Mean Average: %.3f degrees' %stat.mean(lat))
    plt.plot(time, [stat.mean(lat)-stat.stdev(lat)]*len(time), 'g--', label = 'Standard Deviation: %.5f degrees' %stat.stdev(lat))
    plt.plot(time, [stat.mean(lat)+stat.stdev(lat)]*len(time), 'g--')
    plt.legend()

    figtimelong = plt.figure()
    figtimelong.suptitle('Base Longitude vs Time')
    plt.axis([0, time[len(time)-1], stat.mean(longitude)-3*stat.stdev(longitude),stat.mean(longitude)+1*stat.stdev(longitude)])
    plt.xlabel('Time (s)')
    plt.ylabel('Longitude (Degrees)')
    plt.scatter(time, longitude)
    plt.plot(time, [stat.mean(longitude)]*len(time), 'r--', label = 'Mean Average: %.3f degrees' %stat.mean(longitude))
    plt.plot(time, [stat.mean(longitude)-stat.stdev(longitude)]*len(time), 'g--', label = 'Standard Deviation: %.5f degrees' %stat.stdev(longitude))
    plt.plot(time, [stat.mean(longitude)+stat.stdev(longitude)]*len(time), 'g--')
    plt.legend()

    figtimealt = plt.figure()
    figtimealt.suptitle('Base Altitude vs Time')
    plt.axis([0, time[len(time)-1], stat.mean(alt)-2*stat.stdev(alt),stat.mean(alt)+2*stat.stdev(alt)])
    plt.xlabel('Time (s)')
    plt.ylabel('Altitude (Meters)')
    plt.scatter(time, alt)
    plt.plot(time, [stat.mean(alt)]*len(time), 'r--', label = 'Mean Average: %.3f m' %stat.mean(alt))
    plt.plot(time, [stat.mean(alt)-stat.stdev(alt)]*len(time), 'g--', label = 'Standard Deviation: %.5f m' %stat.stdev(alt))
    plt.plot(time, [stat.mean(alt)+stat.stdev(alt)]*len(time), 'g--')
    plt.legend()

    figbase_horiz_acc = plt.figure()
    figbase_horiz_acc.suptitle('Base Horizontal Accuracy Estimate')
    plt.axis([0, time[len(time)-1], stat.mean(base_horiz_acc)-2*stat.stdev(base_horiz_acc),stat.mean(base_horiz_acc)+2*stat.stdev(base_horiz_acc)])
    plt.xlabel('Time (s)')
    plt.ylabel('Horizontal Accuracy (m)')
    plt.scatter(time, base_horiz_acc)
    plt.plot(time, [stat.mean(base_horiz_acc)]*len(time), 'r--', label = 'Mean Average: %.3f m' %stat.mean(base_horiz_acc))
    plt.plot(time, [stat.mean(base_horiz_acc)-stat.stdev(base_horiz_acc)]*len(time), 'g--', label = 'Standard Deviation: %.5f m' %stat.stdev(base_horiz_acc))
    plt.plot(time, [stat.mean(base_horiz_acc)+stat.stdev(base_horiz_acc)]*len(time), 'g--')
    plt.legend()

    gmap_base_latitude_longitude = gmplot.GoogleMapPlotter(stat.mean(lat), stat.mean(longitude), 23)
    gmap_base_latitude_longitude.scatter(lat, longitude, color='b')
    gmap_base_latitude_longitude.draw('/home/magicc/rtk_tests/gnssvsrtk/mar03_2020walkperimter/base_lat_long.html')

    fig_base_latitude_longitude = plt.figure()
    fig_base_latitude_longitude.suptitle('Base Latitude vs Longitude')
    plt.axis([stat.mean(longitude)-4*stat.stdev(longitude), stat.mean(longitude)+2*stat.stdev(longitude), stat.mean(lat)-1*stat.stdev(lat),stat.mean(lat)+3*stat.stdev(lat)])
    plt.xlabel('Longitude (Degrees)')
    plt.ylabel('Latitude (Degrees)')
    plt.scatter(longitude, lat)
    plt.legend()



    plt.show()
    # ani = animate(struct.variable[0])

    #arrow(path+name)

def init():
    print("Init Function Called")

def updateNED(relPosNED, *fargs):
    "Called updateNED function"
    ax = fargs[1]
    # print(relPosNED)
    ax.scatter(relPosNED[0], relPosNED[1], relPosNED[2], 'b.')



#Animate
def animate(variables):
    print("Called Animate Function")
    truevariables = rearrange(variables)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    print(truevariables[0])
    ani = animation.FuncAnimation(fig, updateNED, frames=truevariables, init_func=init, fargs = (fig, ax) , blit=False )
    plt.show()
    set_trace()
    return ani

def rearrange(variables):
    truevariables = []
    for i in range(len(variables[0])):
        truevariables.append([variables[0][i], variables[1][i], variables[2][i]])
    print(truevariables)
    #set_trace()
    return truevariables


#plots an arrow on the figure
def arrow(baglocation):
    bag = rosbag.Bag(baglocation)
    
    #Get arrowlength array
    arrowLength = get_variables(bag, "/base/RelPos", "arrowLength")
    #Get arrowRPY and extract P and Y
    arrowRPY = get_variables(bag, "/base/RelPos", "arrowRPY")
    #Get arrowNED
    arrowNED = get_variables(bag, "/base/RelPos", "arrowNED")
    relPosNED = []
    #Get RelPosNED
    relPosNED = get_variables(bag, "/base/RelPos", "relPosNED")
    #Create a new 3d plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(relPosNED[0], relPosNED[1], relPosNED[2], arrowNED[0], arrowNED[1], arrowNED[2])

    #Do quiver(arrowbaseNED[0], arrowbaseNED[1], arrowbaseNED[2], arrowN, arrowE, arrowD)
    #Also do a quiver with arrowlength and P Y


def loadXML(filename='params/secondtest.xml'):
    tree = ET.parse(filename)
    return tree

def parseXML(tree):
    figures = []
    variables = []
    #Get the root of the tree
    root = tree.getroot()
    for figure in root:
        print("Figure\n")
        fig = plt.figure()
        print(figure.get('title'))
        for axes in figure:
            if axes.get('type') == "3d":
                ax = fig.add_subplot(projection='3d')
            elif axes.get('type') == '2d':
                ax=fig.add_subplot(title=axes.get('title'))
            for plot_type in axes:  #Axes types may be scatter or line
                variables.append(rosplot(ax ,plot_type))
            ax.set_title(axes.get('title'))
        figures.append(fig)
    
    mystruct = namedtuple("mystruct", "figure, variable")
    # print(variables)
    returning = mystruct(figures, variables)
    return returning

def rosplot(ax, plot_type):

    variables = []
    axistitles = []

    #For each axis
    for axis in plot_type:

        print(axis.tag+"\n")

        #Create rosbag
        bag = rosbag.Bag(axis.find('path').text+axis.find('bag').text)

        #For each axis we append variables and axistitles
        variables.append(get_variables(bag, axis.findtext('topic'), axis.findtext('section')))
        if(axis.get('title')==None):
            axistitles.append(axis.findtext('topic')+"/"+axis.findtext('section'))
        else:
            axistitles.append(axis.get('title'))

    if(len(variables)==2):
        #print("2D")
        plot_2d(variables, axistitles, ax, plot_type.tag, plot_type.get('color'), plot_type.get('marker'), plot_type.get('line'))

    elif(len(variables)==3):
        #print("3D")
        plot_3d(variables, axistitles, ax, plot_type.tag, plot_type.get('color'), plot_type.get('marker'))
    else:
        print("Error: Too many axis")
    print("Rosplot variables: ")
    # print(variables)
    #set_trace()
    return variables

def plot_3d(variables, axistitles, ax, plot_type = 'scatter', color='b', m='.', line=''):
    ax.set_xlabel(axistitles[0])
    ax.set_ylabel(axistitles[1])
    ax.set_zlabel(axistitles[2])
    ax.set_title("Test")
    eval('ax.'+plot_type+"(variables[0], variables[1], variables[2], c=color, marker=m)")
    plt.show()

def plot_2d(variables, axistitles = ['Axis 1', 'Axis 2'], title = 'No Title', plot_type = 'scatter', color='b', marker='.', line=''):
    plt.xlabel(axistitles[0])
    plt.ylabel(axistitles[1])
    #plt.suptitle(title)
    plt.plot(variables[0], variables[1], color+marker+line)
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
    #print("get_variables variables")
    # print(variable)
    #set_trace()
    return variable

        
def get_section(msg, section, t=0):
    if section == 'relPosN':
        return msg.relPosNED[0]+msg.relPosHPNED[0]
    elif section == 'relPosE':
        return msg.relPosNED[1]+msg.relPosHPNED[1]
    elif section == 'relPosD':
        return msg.relPosNED[2]+msg.relPosHPNED[2]
    elif section == 'time' or section == 'rosbagtime':
        return [t.secs, t.nsecs]
    elif section == 'Yaw':
        return msg.arrowRPY[2]
    elif section == 'Pitch':
        return msg.arrowRPY[1]
    elif section == 'posN' :
        return msg.position[0]
    elif section == 'lat':
        return msg.lla[0]
    elif section == 'long':
        return msg.lla[1]
    elif section == 'alt':
        return msg.lla[2]
    elif section == '':
        return msg
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