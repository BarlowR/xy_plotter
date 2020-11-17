import path_utility as pu
from text_printing import hershey_text_interpreter as hti
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import gcode_interpreter as gci



if __name__ == "__main__":

	chars = []

	for index, letter in enumerate(" abcdefghijklmnopqrstuvwxyz"):
		if index >0:
			padding = " " * (4-len(str(index)))
			chars.append((letter, padding + str(index)))
	
	
	letters = hti.HersheyFonts("./text_printing/hershey/hershey.txt", chars)

	fig, ax = plt.subplots()
		
	plt.xlim(0, 70)
	plt.ylim(0, 70)

	word = []
	cur_x = 0
	for char in "robert":
		start, stop, paths = letters.letter_dict[char]
		paths = pu.translate_all_paths(paths, cur_x, 0)
		word += paths
		cur_x += stop-start
	
	word = pu.invert_all_paths(word, 3)

	word = pu.scale_all_paths(word, 70, 70)


	pu.plot_paths(word, ax)

	plt.show()

	gci.generate_gcode("robert", word)