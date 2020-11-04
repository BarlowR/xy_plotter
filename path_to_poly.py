import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy



def path_to_polygon(path, distance_threshold=-1):
	#path must have min length of 3

	
	# if the threshold value isn't given, compute it based on path length. These constants seem to work relatively well in practice
	if (distance_threshold == -1):
		distance_threshold = int(np.sqrt(len(path))/20)+.2

	error_sum = 0
	max_error_sum = -1
	best_approx = {}

	node_from_start = 0

	for node in path:


		#we want to try a couple different starting nodes, as the first node in the path is never removed from the set.  
		starting_node_num = 1
		if starting_node_num > 50: starting_node_num = 50;


		if (node_from_start > starting_node_num):
			break
		else:	
			node_from_start += 1


		#reset our variables
		minimized_path = copy.deepcopy(path)
		start_node = node
		P1 = node
		error_sum = 0
		closed = False;
		
		#iterate through all nodes and look for lines between that can approximate intermediate nodes within the given threshold. 
		while not closed:
			loading_bar = int(10*(1- len(minimized_path)/len(path))) * "#"
			#print(loading_bar)

			#set our initial mid and end points along the path
			midP = minimized_path[P1]
			P2 = midP

			max_node_distance = 0

			line_error_sum = 0

			# while we haven't exceded our max node to line distance, figure out the sum of distance of points between P1 and P2 
			while max_node_distance < (distance_threshold**2) and P1 != P2:
				#print("max_node_distance < (distance_threshold**2) and P1 != P2")

				#reset max_node_distance
				max_node_distance = 0
				line_error_sum = 0;

				#iterate aolong all midpoints between P1 and P2
				while midP != P2:
					#print("midP != P2")
					#print(len(minimized_path))
					
					#calculate distance_squared from the midpoint to the line (P1 to P2)
					midP_dist = dist_squared_point_to_line(P1, P2, midP)

					#add this distance squared to the error sum
					line_error_sum += midP_dist

					#if the error is greater than our previous max error, increase our previous max error
					if midP_dist > max_node_distance: max_node_distance = midP_dist

					#move the midpoint along to the next vertex on the path
					midP = minimized_path[midP]

				

				#check if we have a closed path			
				if P2 == start_node: 
					#print("closed")
					closed = True
					break

				#set the endpoint to the next node in the path	
				P2 = minimized_path[P2]	
				

				#set the intermediate point to the node after the start node
				midP = minimized_path[P1]
			
			#check if we have a closed path
			if P2 == start_node: 
					#print("closed")
					closed = True
					break

			#once we exit from the while loop, check if (sqrt(max_node_distance) has excedded the threshold. If so, , make a new node from P1 to P2 and remove all nodes between P1 and P2
			if (max_node_distance > (distance_threshold**2)):
				minimized_path[P1] = P2
				
				while midP != P2:
					midPtemp = minimized_path[midP]
					minimized_path.pop(midP)
					midP = midPtemp
			elif (P1 == P2): 
				print("We really shouldn't be here")
				closed = True

			#increase our path error sum by our line error sum
			error_sum += line_error_sum

			#set our new starting node
			P1 = P2



		#once we have a closed loop, check if our total error is less than the previous approximations. 
		#if it is, save the new minimized total error and the minimized path network
		if error_sum < max_error_sum or max_error_sum == -1:
			max_error_sum = error_sum
			best_approx = minimized_path


			element1 = minimized_path[start_node] 

		#print(error_sum)
	#print(max_error_sum/len(best_approx))
	return (best_approx)
			


#h = 2A/b
#h^2 = (2A)^2 / b^2
#https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points


def dist_squared_point_to_line(P1, P2, midP):


	x0, y0 = midP
	x1, y1 = P1
	x2, y2 = P2

	area_squared_of_triangle = (x0*(y2-y1) - y0*(x2-x1) + x2*y1 - y2*x1)**2
	distance_squared_p1_to_p2 = (y2-y1)**2 + (x2-x1)**2

	return area_squared_of_triangle/distance_squared_p1_to_p2

def plot_polygon(path, ax, linewidth = 2, clr = "blue"):
	polygon = []
	for node in path:
		polygon.append(np.asarray(node)-.5)
	poly = patches.Polygon(polygon, fill = False, ls = '-', closed = True, lw = linewidth, color = clr)
	ax.add_patch(poly)

