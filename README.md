# rosbag_parser
There are two python scripts used to parse rosbags.  The rosbag_parser.py will read the rosbag and create variables for whichever values you need.  The rosbag_data.py will import those variables and plot them.

Modifications need to be made depending on what data from the rosbag you want to analyze.

In rosbag_parser.py:
Be sure that the bag variable is pointed to the file of the rosbag.
In the for loop specify the topic and variables you need.  Also initialize arrays holding those variables.

In rosbag_data.py:
Change the variable names to match the variables selected in the parser.
The rest of the script can be modified to plot and calculate whatever is needed from the selected variables.
