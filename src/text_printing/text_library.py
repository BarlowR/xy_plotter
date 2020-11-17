import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class draw_letter:

	def __init__(self, figure, axis):

		figure.canvas.mpl_connect('motion_notify_event', self.mouse_move)
		figure.canvas.mpl_connect('button_press_event', self.mouse_click)

		self.mouse_position = (0,0)
		self.segment = []
		self.letter = []
		self.ax = axis
		self.figure = figure


	def mouse_move(self, event):
	    self.mouse_position = (event.xdata, event.ydata)
	    #print(self.mouse_position)	
	    

	def mouse_click(self, event):
		
		print(event.button)
		if (event.button == 1):
			self.segment.append(self.mouse_position)
			print(self.mouse_position)
		elif (event.button == 3):
			self.letter.append(self.segment)
			self.segment = []
		
		for seg in self.letter + [self.segment]:
			if (len(seg)>0):
				poly = patches.Polygon(seg, fill = False, ls = '-', closed = False, lw = 1, color = 'red')
				ax.add_patch(poly)
		self.figure.show()









if __name__ == "__main__":



	fig, ax = plt.subplots()
		
	plt.xlim(0, 5)
	plt.ylim(0, 5)

	draw_ltr = draw_letter(fig, ax)




	

	plt.axis('equal')
	plt.show()

