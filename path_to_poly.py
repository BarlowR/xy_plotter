import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import copy



def path_to_polygon(path, distance_threshold):
	#path must have min length of 3
	
	error_sum = 0
	max_error_sum = -1
	best_approx = {}

	for node in path:
		#reset our variables
		minimized_path = copy.deepcopy(path)
		print(" ")
		print(minimized_path)
		start_node = node
		P1 = node
		error_sum = 0
		closed = False;
		
		#iterate through nodes, removing nodes if they are within a certain distance of a line from a prior to a later node
		while not closed:


			#set our initial mid and end points along the path
			midP = minimized_path[P1]
			P2 = minimized_path[midP]

			max_node_distance = 0

			line_error_sum = 0

			# while we haven't exceded our max node to line distance, figure out the sum of distance of points between P1 and P2 
			while max_node_distance < (distance_threshold**2) and P1 != P2:

				#reset max_node_distance
				max_node_distance = 0
				line_error_sum = 0;

				#iterate aolong all midpoints between P1 and P2
				while midP != P2:

					#calculate distance_squared from the midpoint to the line (P1 to P2)
					midP_dist = dist_squared_point_to_line(P1, P2, midP)

					#add this distance squared to the error sum
					line_error_sum += midP_dist

					#if the error is greater than our previous max error, increase our previous max error
					if midP_dist > max_node_distance: max_node_distance = midP_dist

					#move the midpoint along to the next vertex on the path
					midP = minimized_path[midP]

				#set the endpoint to the next node in the path
				P2 = minimized_path[P2]

				#check if we have a closed path yet
				
				print(P1)
				print(midP)
				print(P2)
				print(start_node)
				print(minimized_path[start_node])
				print(" ")
				if P2 == start_node: 
					print("closed")
					closed = True
					break

				#set the intermediate point to the node after the start node
				midP = minimized_path[P1]
			
			#once we exit from the while loop (sqrt(max_node_distance) has excedded the threshold), make a new node from P1 to P2
			minimized_path[P1] = P2

			#remove all nodes between P1 and P2
			
			while midP != P2:

				'''print(P1)
				print(midP)
				print(P2)
				print(" ")'''

				midPtemp = minimized_path[midP]
				minimized_path.pop(midP)
				midP = midPtemp

			#increase our path error sum by our line error sum
			error_sum += line_error_sum

			#set our new starting node
			P1 = P2

		#once we have a closed loop, check if our total error is less than the previous approximations. 
		#if it is, save the new minimized total error and the minimized path network
		if error_sum < max_error_sum or max_error_sum == -1:
			max_error_sum = error_sum
			best_approx = minimized_path

		break
	print(max_error_sum)
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

