import matplotlib.patches as patches
import numpy as np

#display the closed path as a polygon on the given matplotlib figure
def plot_polygon(path, ax, linewidth = 2, clr = "blue"):
	polygon = []
	for node in path:
		polygon.append(np.asarray(path[node])-.5)
	poly = patches.Polygon(polygon, fill = False, ls = '-', closed = False, lw = linewidth, color = clr)
	ax.add_patch(poly)

def plot_polygons(paths, ax, linewidth = 2, clr = "blue"):
	for path in paths:
		plot_polygon(path, ax, linewidth, clr)

def plot_paths(paths, ax, linewidth = 2, clr = "blue"):
	for path_list in paths:
		for path in path_list:
			key = path
			value = path_list[key]

			x, y = key
			x1, y1 = value
			dx = x1-x
			dy = y1-y

			arrow = patches.Arrow(x, y, dx, dy, width = linewidth, color = clr)
			ax.add_patch(arrow)





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
	
	#print(min_x, min_y, max_x, max_y)

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



def scale_all_paths(paths, max_width, max_height, bounds = None):
	scaled_paths = []

	if bounds is None:
		min_x=None
		min_y=None
		max_x=None
		max_y=None

		for path in paths:
			for node in path.keys():
				if min_x is None or node[0] < min_x : min_x = node[0]
				elif max_x is None or node[0] > max_x : max_x = node[0]

				if min_y is None or node[1] < min_y : min_y = node[1]
				elif max_y is None or node[1] > max_y : max_y = node[1]

			for node in path.values():
				if min_x is None or node[0] < min_x : min_x = node[0]
				elif max_x is None or node[0] > max_x : max_x = node[0]

				if min_y is None or node[1] < min_y : min_y = node[1]
				elif max_y is None or node[1] > max_y : max_y = node[1]

		bounds = (min_x, min_y, max_x, max_y)

	for path in paths:
		scaled_paths.append(scale_path(path, max_width, max_height, bounds))

	return scaled_paths


def invert_path(path, max_y = None):

	inverted_path = {}

	for node in path:
		if max_y is None or node[1] > max_y : max_y = node[1]


	for node in path:

		key = node
		value = path[key]

		x, y = key
		x1, y1 = value

		inverted_path[(x, -y)] = (x1, -y1)

	return inverted_path


def invert_all_paths(paths, max_y = None):
	inverted_paths = []

	for path in paths:
		inverted_paths.append(invert_path(path, max_y))

	return inverted_paths


def translate_path(path, x_trans, y_trans):
	translated_path = {}

	for node in path:
		key = node
		value = path[key]
		x, y = key
		x1, y1 = value
		translated_path[(x+x_trans, y+y_trans)] = (x1+x_trans, y1+y_trans)

	return translated_path


def translate_all_paths(paths, x_trans, y_trans):
	translated_paths = []

	for path in paths:
		translated_paths.append(translate_path(path, x_trans, y_trans))

	return translated_paths