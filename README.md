# rosbag_parser
There are several python scripts used to parse rosbags.  The rosbag_parser.py will read the rosbag and create variables for whichever values you need. Specifically, there is a function within the file called get_variables that does this.  The other files  will import those variables to run their various different analyses.

Modifications need to be made depending on what data from the rosbag you want to analyze.

In rosbag_parser.py:
Be sure that the bag variable is pointed to the file of the rosbag.
In the for loop specify the topic and variables you need.  Also initialize arrays holding those variables.

In other files:
Change the variable names to match the variables selected in the parser.
The rest of the scripts can be modified to plot and calculate whatever is needed from the selected variables.
