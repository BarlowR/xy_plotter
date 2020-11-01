import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


class OutlinePath:

	dir_select = {
		(0, 0, 
		 1, 0) : 1, 

		(1, 0,
		 1, 0) : 0,

		(1, 1, 
		 1, 0) : -1,

		(0, 1,
		 1, 0) : 1,
		}

	vertex_shift = {
	#key is direction of motion along path; > is 0, ^ is 1, < is 2, v is 3. Element is tuple of vertex x,y index change
		0 : (1, 0),
		1 : (0, -1),
		2 : (-1, 0),
		3 : (0, 1)
	}



	@staticmethod
	def outline_outer_image(img):
		#img is a numpy boolean array of a black and white image, where black pixels are 1 and white pixels are 0
		#prior_paths is a list of directed graphs, with each element corresponding to a boundry outline in the original image
		


		path = {}

		current_vertex = OutlinePath.find_start_vertex(img)

		if current_vertex is not None:
			first_vertex = current_vertex
			last_vertex = None
			current_theta = 0;
			current_grid = OutlinePath.get_grid(current_vertex, img)

			for i in range(4):
				grid = OutlinePath.dir_trans(i, current_grid)
				if grid in OutlinePath.dir_select:
					current_theta = i
					break


			while not (first_vertex == last_vertex):

				rotated_grid = OutlinePath.dir_trans(current_theta, current_grid)
				current_theta = (current_theta + OutlinePath.dir_select[rotated_grid])%4

				vert_x, vert_y = current_vertex
				x_shift, y_shift = OutlinePath.vertex_shift[current_theta]
				new_vertex = (vert_x + x_shift, vert_y + y_shift)


				path[current_vertex] = new_vertex


				current_vertex = new_vertex
				current_grid = OutlinePath.get_grid(current_vertex, img)
				last_vertex = current_vertex

				
				if (current_vertex in path) and (current_vertex != first_vertex):
					next_vertex = current_vertex
					while next_vertex is not None:
						next_vertex = path.pop(next_vertex, None)

			inverted_image = OutlinePath.invert_closed_path(path, img)
			
			return [path] + OutlinePath.outline_outer_image(inverted_image)
		else: return []

			


		



		

	def find_start_vertex(img):
		rows, columns = img.shape
		for row_index in range(1,rows):
			for column_index in range(1,columns):
				a, b, c, d = OutlinePath.get_grid((column_index, row_index), img)
				if ((a or b or c or d ) and not (a and b and c and d)):
						return (column_index, row_index)

		return None
		

	@staticmethod
	def dir_trans(theta, grid):
		#theta is direction of motion along path; > is 0, ^ is 1, < is 2, v is 3
		# grid is a tuple of the boolean pixels surrounding the current vertex;
		#	 for a grid that has pixel positions [0,1] the corresping tuple would be (0,1,2,3) 
		#                            			 [2,3] 
		# this method returns the pixel grid rotated by the corresponding theta; 
		#    for a n input of 2 and a pixel grid of [0,0] the resulting grid would be [0,0] and the tuplle would be (0,0,0,1)
		#                                           [1,0]                             [0,1]                       

		direction_transform = {
			0 : (grid[1], grid[3], grid[0], grid[2]),
			1 : (grid[0], grid[1], grid[2], grid[3]),
			2 : (grid[2], grid[0], grid[3], grid[1]),
			3 : (grid[3], grid[2], grid[1], grid[0])
		}

		return direction_transform[theta]

	@staticmethod
	def get_grid(vertex, img):
		x, y = vertex
		return (
			img[y-1][x-1], #top left
			img[y-1][x],   #top right
			img[y][x-1],   #bottom left
			img[y][x]      #bottom right
			)
	
	@staticmethod
	def print_grid(grid):
		# grid is a tuple of the boolean pixels surrounding the current vertex;
		#	 for a grid that has pixel positions [0,1] the corresping tuple would be (0,1,2,3) 
		#                            			 [2,3] 

		grid = "[" + str(grid[0]) + " " + str(grid[1]) + "]\n[" + str(grid[2]) + " " + str(grid[3]) + "]"
		print(grid)
		return grid

	@staticmethod
	def print_grid_theta(theta, grid):
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

	@staticmethod
	def img_to_bool_array(img):
		img_array = np.asarray(img)
		bool_array = np.where(img_array< 1, np.zeros(img_array.shape), 1)

		padding = np.zeros((bool_array.shape[0]+2, img_array.shape[1]+2))
		padding[1:bool_array.shape[0]+1, 1:bool_array.shape[1]+1] = bool_array
		return padding


	@staticmethod
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

	def outline_path(path):
		for node in path:
			plt.scatter(node[0]-.5, node[1]-.5, color = 'red')	


if __name__ == "__main__":

	image = Image.open('imageSmall.png')
	img_array = OutlinePath.img_to_bool_array(image)
	paths = OutlinePath.outline_outer_image(img_array)
	for path in paths:
		OutlinePath.outline_path(path)

	plt.show()
	#print(paths)




