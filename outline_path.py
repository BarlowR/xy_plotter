import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

import path_to_poly as p2p




dir_select = {
#based on a 2x2 grid of pixels, determine how to change direction
	(0, 0, 
	 1, 0) : 1,  #turn left

	(1, 0,
	 1, 0) : 0,  #go straight

	(1, 1, 
	 1, 0) : -1, #turn right 

	(0, 1,
	 1, 0) : 1,  #turn left
	}



vertex_shift = {
#key is direction of motion along path; > is 0, ^ is 1, < is 2, v is 3. Element is tuple of vertex x,y index change
	0 : (1, 0),
	1 : (0, -1),
	2 : (-1, 0),
	3 : (0, 1)
}





	#Recursively finds all paths along black/white borders within the image given, and returns them as a list of directed graphs. 	
def outline_outer_image(img, path_num = -1, min_path_length = -1):
	#img is a numpy boolean array of a black and white image, where black pixels are 1 and white pixels are 0. 
	#path_num defines max number of paths to return. 
	#min_path_length defines the minimum path length to include in the resulting path list

	if (min_path_length == -1): 
		min_path_length = (img.shape[0]+img.shape[1])/5
	path = {}

	#Grab top leftmost vertex along a border
	current_vertex = find_start_vertex(img)



	# if there exist any pixels to trace and we don't already have enough paths, trace the outline of the path
	#else, return an empty list

	if (current_vertex is not None and path_num != 0):

		if (path_num > 0):
			print("#" * path_num)
		else:
			print("starting path")

		#setup the path tracing variables
		first_vertex = current_vertex
		last_vertex = None
		current_theta = 0;
		current_grid = get_grid(current_vertex, img)

		# our path tracing algorithm only follows outlines with the black pixels on the left side & white pixels on the right, 
		# this takes our initial vertex and orients our direction such that the black pixels are on the left.
		for i in range(4):
			grid = dir_trans(i, current_grid)
			if grid in dir_select:
				current_theta = i
				break

		# run this loop while we have a closed loop in our path

		while True:


			#take a 2x2 grid of pixels surrounding our current vertex and rotate it to our path-tracing direction
			rotated_grid = dir_trans(current_theta, current_grid)

			#based on the rotated grid, determine what direction to take & update our direction
			current_theta = (current_theta + dir_select[rotated_grid])%4

			#determine our next vertex location
			vert_x, vert_y = current_vertex
			x_shift, y_shift = vertex_shift[current_theta]
			new_vertex = (vert_x + x_shift, vert_y + y_shift)

			#add our (current vertex : new vertex) pair to the path directed graph 
			path[current_vertex] = new_vertex

			#move our vertex along and pull the new pixel grid
			current_vertex = new_vertex
			current_grid = get_grid(current_vertex, img)
			last_vertex = current_vertex

			
			# check if we've been at this vertex before. 
			# If it's our starting vertex, then we exit the loop. 
			# Otherwise, we've traced an internal loop within our outline, which we don't want. 
			# If this is the case, we pop all values until we've removed the internal loop.
			if (current_vertex == first_vertex):
					break
			elif (current_vertex in path):
					next_vertex = current_vertex
					while next_vertex is not None:
						next_vertex = path.pop(next_vertex, None)

		# Once we have a closed loop, then we invert all of the pixels within the loop, which removes the outline from the image.
		inverted_image = invert_closed_path(path, img)
		

		return_list = []

		# if our path length is long enough, we add it to the list of paths and decremend the number of paths left to add
		if len(path) > min_path_length:
			return_list += [path]
			path_num -= 1
		#else: print("path too short")	

		# Recursively calculate the next outline
		if path_num > 0:
			return_list += outline_outer_image(inverted_image, path_num = path_num, min_path_length = min_path_length)
		elif path_num < 0:
			return_list += outline_outer_image(inverted_image, min_path_length = min_path_length)

		return return_list
	
	else: return []

		


	



	
#iterate over all pixels until we find a pixel vertex along a black/white border
def find_start_vertex(img):
	rows, columns = img.shape
	for row_index in range(1,rows):
		for column_index in range(1,columns):
			a, b, c, d = get_grid((column_index, row_index), img)
			if ((a or b or c or d ) and not (a and b and c and d)):
					return (column_index, row_index)

	return None
	



# return a given pixel grid rotated by the given theta direction; 
# for a theta input of 2 and a pixel grid of [1,0] the resulting grid would be [0,0] and the tuplle would be (0,0,1,1)
#                                            [1,0]                             [1,1]                       

def dir_trans(theta, grid):
	# theta is direction of motion along path; > is 0, ^ is 1, < is 2, v is 3
	# grid is a tuple of the boolean pixels surrounding the current vertex;
	#	 for a grid that has pixel positions [0,1] the corresping tuple would be (0,1,2,3) 
	#                                        [2,3]
		
	direction_transform = {
		0 : (grid[1], grid[3], grid[0], grid[2]),
		1 : (grid[0], grid[1], grid[2], grid[3]),
		2 : (grid[2], grid[0], grid[3], grid[1]),
		3 : (grid[3], grid[2], grid[1], grid[0])
	}

	return direction_transform[theta]


# based on vertex and a bolean image array, return the 2x2 grid of pixel values surrounding the vertex

def get_grid(vertex, img):
	x, y = vertex
	return (
		img[y-1][x-1], #top left
		img[y-1][x],   #top right
		img[y][x-1],   #bottom left
		img[y][x]      #bottom right
		)


# print a given pixel grid

def print_grid(grid):
	# grid is a tuple of the boolean pixels surrounding the current vertex;
	#	 for a grid that has pixel positions [0,1] the corresping tuple would be (0,1,2,3) 
	#                            			 [2,3] 

	grid = "[" + str(grid[0]) + " " + str(grid[1]) + "]\n[" + str(grid[2]) + " " + str(grid[3]) + "]"
	print(grid)
	return grid


#print a given pixel grid with a given theta

def print_grid_theta(theta, grid):
	# theta
	# grid is a tuple of the boolean pixels surrounding the current vertex;
	#	 for a grid that has pixel positions [0,1] the corresping tuple would be (0,1,2,3) 
	#                            			 [2,3] 
	grid_direction = {
		1 : "[" + str(grid[0]) + "   " + str(grid[1]) + "]\n     ^   \n[" + str(grid[2]) + " | " + str(grid[3]) + "]",
		3 : "[" + str(grid[0]) + " | " + str(grid[1]) + "]\n     v   \n[" + str(grid[2]) + "   " + str(grid[3]) + "]",
		0 : "[" + str(grid[0]) + "   " + str(grid[1]) + "]\n->     \n[" + str(grid[2]) + "   " + str(grid[3]) + "]",
		2 : "[" + str(grid[0]) + "   " + str(grid[1]) + "]\n          <-\n[" + str(grid[2]) + "   " + str(grid[3]) + "]",
		}
	print(grid_direction[theta])
	return grid

#take in a PIL image and turn it into b&w image with pixel values in (0,1) and a white pixel border. 

def img_to_bool_array(img, threshold):
	#threshold determines the cutoff for black v white pixels, should be between 255 and 0. 200 seems to work well for artifact-y jpgs 
	img_array = np.asarray(img.convert('L'))
	bool_array = np.where(img_array < threshold, np.ones(img_array.shape), 0)
	padding = np.zeros((bool_array.shape[0]+2, bool_array.shape[1]+2))
	padding[1:bool_array.shape[0]+1, 1:bool_array.shape[1]+1] = bool_array
	return padding


#given an image and a closed path, invert all pixels within the given path

def invert_closed_path(path, img):
	y_dim, x_dim = img.shape
	inverted_image = img

	invert = 0

	
	for j in range(y_dim):
		for i in range(x_dim):
			if ((i, j) in path) and ((i, j+1) in path): 
				if (path[(i, j)] == (i, j+1) or path[(i, j+1)] == (i, j)): invert = not invert

			if invert : inverted_image[j][i] = not inverted_image[j][i]
		invert = 0

	return inverted_image	

#take a path and scatter plot all nodes. Useful for visualizing the path ontop of the initial image

def outline_path(path, clr):
	for node in path:
		plt.scatter(node[0]-.5, node[1]-.5, color = clr)	

#return n = num_to_keep longest paths in the list of paths. 

def cull_paths(paths, num_to_keep):
	paths.sort(reverse = True, key=len)
	return paths[:num_to_keep]




if __name__ == "__main__":

	image = Image.open('man.jpg')
	plt.subplot(1,2,1)
	plt.imshow(image, 'gray')
	img_array = img_to_bool_array(image, 180)
	ax = plt.subplot(1,2,2)
	plt.imshow(img_array, 'gray')

	
	paths = outline_outer_image(img_array, min_path_length = 3)


	total_initial_length = 0
	total_minimized_length = 0
	loading = ""

	for path in paths:
		loading += "#"
		print(loading + "path length " + str(len(path)))

		short_path = p2p.path_to_polygon(path, 0.2)
		total_initial_length += len(path)

		total_minimized_length += len(short_path)
		
		#outline_path(path, clr = (1, 0,0, 0.1))
		
		p2p.plot_polygon(short_path, ax)

	print(total_minimized_length/total_initial_length)
	plt.show()
	#print(paths)'''




