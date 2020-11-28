import path_utility as pu
from text_printing import hershey_text_interpreter as hti
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import gcode_interpreter as gci



if __name__ == "__main__":
	
	

	while True:
		letters = hti.HersheyFonts()

		fig, ax = plt.subplots()
			
		plt.xlim(-25, 125)
		plt.ylim(-100, 100)

		symbol = []
		cur_x = 0

		line = 0

		for char in "Hello Wesley! \nFrom Rob":

			if char == "\n":
				cur_x = 0
				line +=1
			else:
				start, stop, paths = letters.letter_dict[char]
				paths = pu.translate_all_paths(paths, cur_x, line *25)
				symbol += paths
				cur_x += stop-start

		
		symbol = pu.invert_all_paths(symbol, 3)

		pu.plot_paths(symbol, ax)

		plt.show()

