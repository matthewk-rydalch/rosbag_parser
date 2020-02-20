from rosbag_parser import Parser
import matplotlib.pyplot as plt
from IPython.core.debugger import set_trace
import rosbag
import numpy as np

def main():
	
	parser = Parser()

	filename = 'default.bag'
	bag = rosbag.Bag('../../data/boatLanding_sim/' + filename)

	vals = parser.get_variables(bag)
	bag.close

	#est = estimate
	#each returning vextor is of the following form
	#[time, north, east, altitude]
	est, truth, command, est_error, truth_error = get_vals(vals)

	plotter(est, truth, command, est_error, truth_error)
	return est, truth, command, est_error, truth_error

def get_vals(vals):

	#o is for odom(estimate), t for throttled(truth), and c for high level command
	#to is time of odom
	#xot is the x position of odom measurement at time t
	t_odom = np.squeeze(vals.odom_sec+np.array([vals.odom_nsec])*1e-9)
	Xt_odom = np.array(vals.odom_pos).T
	t_thr = np.squeeze(vals.thr_sec+np.array([vals.thr_nsec])*1e-9)
	Xt_thr = np.array(vals.thr_pos).T
	t_c = np.squeeze(vals.wp_sec+np.array([vals.wp_nsec])*1e-9)
	Xt_c = np.array([vals.wp_x, vals.wp_y, vals.wp_z]).T #high level command

	to = t_odom
	xot = Xt_odom[:,0]
	yot = Xt_odom[:,1]
	zot = -Xt_odom[:,2] #flipping sign of z because it is using NED rather than altitude
	est = np.array([to, xot, yot, zot])

	tt = t_thr
	xtt = Xt_thr[:,0]
	ytt = Xt_thr[:,1]
	ztt = -Xt_thr[:,2] #flipping sign of z because it is using NED rather than altitude
	truth = np.array([tt, xtt, ytt, ztt])

	t_points = t_c
	x_points = Xt_c[:,0]
	y_points = Xt_c[:,1]
	z_points = Xt_c[:,2]
	#make commanded position lines rather than points
	tc = [t_points[0]]
	xct = [x_points[0]]
	yct = [y_points[0]]
	zct = [z_points[0]]

	for i in range(1,len(t_points)):
		tc.append(t_points[i])
		tc.append(t_points[i])
		xct.append(x_points[i-1])
		xct.append(x_points[i])
		yct.append(y_points[i-1])
		yct.append(y_points[i])
		zct.append(z_points[i-1])
		zct.append(z_points[i])
	tc = np.array(tc)
	xct = np.array(xct)
	yct = np.array(yct)
	zct = np.array(zct)
	command = np.array([tc, xct, yct, zct])

	#calculate estimation errors
	#get estimated values to line up with true values
	to_align = []
	xo_align = []
	yo_align = []
	zo_align = []
	j = 0
	for i in range(len(tt)):
		while to[j] < tt[i]:
			j = j+1
		
		to_align.append(to[j])
		xo_align.append(xot[j])
		yo_align.append(yot[j])
		zo_align.append(zot[j])

	to_error = np.array(to_align) #estimates error to truth
	xo_error = xo_align-xtt
	yo_error = yo_align-ytt
	zo_error = zo_align-ztt
	est_error = np.array([to_error, xo_error, yo_error, zo_error])

	#calculate positional errors
	#get truth indices to line up with commanded indices
	tt_align = []
	xt_align = []
	yt_align = []
	zt_align = []
	j = 0
	for i in range(len(t_points)-1):
		while tt[j] < t_points[i+1]:
			j = j+1
		
		tt_align.append(tt[j])
		xt_align.append(xtt[j])
		yt_align.append(ytt[j])
		zt_align.append(ztt[j])

	tt_align.append(tt[len(tt)-1])
	xt_align.append(xtt[len(tt)-1])
	yt_align.append(ytt[len(tt)-1])
	zt_align.append(ztt[len(tt)-1])
    
	tt_error = np.array(tt_align) #command error to truth
	xt_error = x_points-xt_align
	yt_error = y_points-yt_align
	zt_error = z_points-zt_align
	truth_error = np.array([tt_error, xt_error, yt_error, zt_error])

	return est, truth, command, est_error, truth_error

def plotter(est, truth, command, est_error, truth_error):
	#est = estimate
	#each returning vextor is of the following form
	#[time, north, east, altitude]
	
	fig1, sub = plt.subplots(3)
	fig1.suptitle("Estimated, Actual, and Commanded Location")
	sub[0].plot(est[0],est[1], label = "estimate")
	sub[0].plot(truth[0],truth[1], label = "truth")	
	sub[0].plot(command[0],command[1], label = "command")	
	sub[0].legend(loc = "upper right")
	sub[0].set_ylabel('x pos [m]')
	sub[1].plot(est[0],est[2], label = "estimate")
	sub[1].plot(truth[0],truth[2], label = "truth")
	sub[1].plot(command[0],command[2], label = "command")
	sub[1].set_ylabel('y pos [m]')
	sub[2].plot(est[0],est[3], label = "estimate")
	sub[2].plot(truth[0],truth[3], label = "truth")
	sub[2].plot(command[0],command[3], label = "command")
	sub[2].set_xlabel('time [s]')
	sub[2].set_ylabel('z pos [m]')

	fig2, sub2 = plt.subplots(3)
	fig2.suptitle("Error")
	sub2[0].plot([0,est_error[0][len(est_error[0])-1]],[0,0], label = "zero", linestyle = '--')
	sub2[0].plot(est_error[0],est_error[1], label = "estimator error")
	sub2[0].scatter(truth_error[0],truth_error[1], color = 'red', label = "truth error")
	sub2[0].set_ylabel('x error [m]')
	sub2[0].legend(loc = "upper left")
	sub2[1].plot([0,est_error[0][len(est_error[0])-1]],[0,0], label = "zero", linestyle = '--')
	sub2[1].plot(est_error[0],est_error[2], label = "estimator error")
	sub2[1].scatter(truth_error[0],truth_error[2], color = 'red', label = "error")
	sub2[1].set_ylabel('y error [m]')
	sub2[2].plot([0,est_error[0][len(est_error[0])-1]],[0,0], label = "zero", linestyle = '--')
	sub2[2].plot(est_error[0],est_error[3], label = "error")
	sub2[2].scatter(truth_error[0],truth_error[3], color = 'red', label = "error")
	sub2[2].set_xlabel('time [s]')
	sub2[2].set_ylabel('z error [m]')

if __name__ == '__main__':
    est, truth, command, est_error, truth_error = main()
