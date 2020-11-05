import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#tweak these variables to match your machine
#these values are in mm/min. I don't plan to include imperial units at this point
XY_feedrate = "2000"
XY_rapid = "2000"
Z_feedrate = "300"

sig_figs = 6




def file_header(file_string):
	file_string += ('''

G21			; Set units to mm
G90			; Absolute positioning
G1 Z1 F100		; Move to clearance level



; XY feedrate:		''' + XY_feedrate + '''
; Z_feedrate: 		''' + Z_feedrate
)
	return file_string








	return file_string


def path_to_gcode(file_string, path):
	
	first_node = True

	for node in path:
		if first_node:
			file_string +=  (
				"G0 Z1 F" + Z_feedrate + "\n" + 
				"G0 X" + str(node[0])[0:sig_figs] + " Y" + str(node[1])[0:sig_figs]  + " F" + XY_rapid + "\n" +
				"G0 Z0 F" + Z_feedrate + "\n"
				)
			first_node = False

		x, y = path[node]
		file_string += "G1 X" + str(x)[0:sig_figs]  + " Y" + str(y)[0:sig_figs]  + " F" + XY_feedrate + "\n"

	file_string += 	(
					"G0 Z1 F" + Z_feedrate + "\n" + 
					"; path finished" + "\n \n"
					)

	return file_string

def path_list_to_gcode(file_string, paths):

	file_string += "; Beginning tracing of " + str(len(paths)) + " closed paths \n \n"

	path_num = 0
	for path in path:
		path_num += 1
		file_string += "; Path " + str(path_num) + "\n"
		file_string = path_to_gcode(file_string, path)







def write_gcode_file(name, file_string, file_extension = ".gcode"):
	file_name = name + file_extension
	file = open(file_name, "w")
	file.write(file_string)

	



