import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#tweak these variables to match your machine
#these values are in mm/min. I don't plan to include imperial units at this point
XY_feedrate = "1500"
XY_rapid = "2000"
Z_feedrate = "7"

sig_figs = 6




def file_header(file_string):
	file_string += ('''

G21			; Set units to mm
G90			; Absolute positioning
G1 Z2 F100		; Move to clearance level



; XY feedrate:		''' + XY_feedrate + '''
; Z_feedrate: 		''' + Z_feedrate
)
	return file_string








	return file_string


def path_to_gcode(file_string, path):
	
	first_node = True

	for node in path:

		if first_node:
			x_pos = str(node[0])
			y_pos = str(node[1])
		else:
			x_pos = str(path[node][0])
			y_pos = str(path[node][1])
		if len(x_pos) > sig_figs: x_pos = x_pos[:sig_figs]
		if len(y_pos) > sig_figs: y_pos = y_pos[:sig_figs]

		if first_node:
			file_string +=  (
				"G0 Z2 F" + Z_feedrate + "\n" + 
				"G0 X" +  x_pos + " Y" + y_pos  + " F" + XY_rapid + "\n" +
				"G0 Z-1 F" + Z_feedrate + "\n"
				)
			first_node = False
			x_pos = str(path[node][0])
			y_pos = str(path[node][1])
			if len(x_pos) > sig_figs: x_pos = x_pos[:sig_figs]
			if len(y_pos) > sig_figs: y_pos = y_pos[:sig_figs]

		file_string += "G1 X" + x_pos  + " Y" + y_pos  + " F" + XY_feedrate + "\n"

	file_string += 	(
					"G0 Z2 F" + Z_feedrate + "\n" + 
					"; path finished" + "\n \n"
					)

	return file_string

def path_list_to_gcode(file_string, paths):

	file_string += "; Beginning tracing of " + str(len(paths)) + " closed paths \n \n"

	path_num = 0
	for path in paths:
		path_num += 1
		file_string += "; Path " + str(path_num) + "\n"
		file_string = path_to_gcode(file_string, path)

	return(file_string)



def write_gcode_file(name, file_string, file_extension = ".gcode"):
	file_name = name + file_extension
	file = open(file_name, "w")
	file.write(file_string)


def generate_gcode(name, paths):
	file_string = file_header("")

	file_string = path_list_to_gcode(file_string, paths)

	write_gcode_file(name, file_string)

	



