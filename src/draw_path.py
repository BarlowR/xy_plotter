import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class DrawPath:

	def __init__(self, figure, axis):


		figure.canvas.mpl_connect('motion_notify_event', self.mouse_move)
		figure.canvas.mpl_connect('button_press_event', self.mouse_click)

		self.mouse_position = (0,0)
		self.segment = []
		self.shape = []
		self.ax = axis
		self.figure = figure


	#when the mouse movies, update the mouse position variables
	def mouse_move(self, event):
	    self.mouse_position = (event.xdata, event.ydata)
	    #print(self.mouse_position)	
	    

	#handle mouseclick events
	def mouse_click(self, event):
		
		#if the left button is clicked, add a node to our path
		if (event.button == 1):
			self.segment.append(self.mouse_position)
			print(self.mouse_position)
		
		#otherwise, if the right mouse button is clicked, finsh that path and add it to our list of paths
		elif (event.button == 3):
			self.shape.append(self.segment)
			self.segment = []
		

		for seg in self.shape + [self.segment]:
			if (len(seg)>0):
				poly = patches.Polygon(seg, fill = False, ls = '-', closed = False, lw = 1, color = 'red')
				ax.add_patch(poly)
		self.figure.show()




if __name__ == "__main__":



	fig, ax = plt.subplots()
		
	plt.xlim(0, 5)
	plt.ylim(0, 5)

	draw_ltr = DrawPath(fig, ax)
	

	plt.axis('equal')
	plt.show()

