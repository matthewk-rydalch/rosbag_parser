from IPython.core.debugger import set_trace
from importlib import reload
import matplotlib.pyplot as plt
import rosbag
import numpy as np
import rosbag_parser

reload(rosbag_parser)

figure = plt.figure()
figure.suptitle("Hello")
plt.show()

#parser = Parser()

#filename = 'rover-10-4-stationary.bag'
#bag = rosbag.Bag('../rtk_tests/stationary/' + filename)

#variables = parser.get_variables(bag, filename)
#