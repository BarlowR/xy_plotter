import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#tweak these variables to match your machine
#these values are in mm/min. I don't plan to include imperial units at this point
XY_feedrate = 2000
Z_feedrate = 300




def file_header(file_string):

	file_string += '''
		G21         ; Set units to mm \n
		G90         ; Absolute positioning \n
		G1 Z1 F100      ; Move to clearance level \n
		'''
	return True


def path_to_gcode(file_string, path):
	
	first_node = True

	


def scale_path(path, max_width, max_height, bounds = None):
	
	if bounds is None:
		min_x=None
		min_y=None
		max_x=None
		max_y=None

		for node in path:
			if min_x is None or node[0] < min_x : min_x = node[0]
			elif max_x is None or node[0] > max_x : max_x = node[0]

			if min_y is None or node[1] < min_y : min_y = node[1]
			elif max_y is None or node[1] > max_y : max_y = node[1]

	else:
		min_x, min_y, max_x, max_y = bounds
	
	scale = 1
	scaled_path = {}


	

	

	print(min_x, min_y, max_x, max_y)

	path_width = max_x - min_x
	path_height = max_y - min_y


	scale_x_percentage = max_width/path_width
	scale_y_percentage = max_height/path_height

	if scale_x_percentage > scale_y_percentage:
		scale = scale_y_percentage
	else: scale = scale_x_percentage


	for node in path:
		key = node
		value = path[key]
		x, y = key
		x1, y1 = value

		x -= min_x
		x1 -= min_x
		y -= min_y
		y1 -= min_y

		x *= scale
		x1 *= scale
		y *= scale 
		y1 *= scale

		scaled_path[(x, y)] = (x1, y1)

	return scaled_path


def invert_path(path, max_y = None):

	inverted_path = {}

	for node in path:
		if max_y is None or node[1] > max_y : max_y = node[1]

		key = node
		value = path[key]

		x, y = key
		x1, y1 = value


	for node in path:

		key = node
		value = path[key]

		x, y = key
		x1, y1 = value

		inverted_path[(x, max_y-y)] = (x1, max_y-y1)

	return inverted_path
