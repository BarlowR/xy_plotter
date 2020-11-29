import path_utility as pu
from text_printing import hershey_text_interpreter as hti
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

import gcode_interpreter as gci

import outline_path

import path_to_poly as p2p



if __name__ == "__main__":
	
	

	
	letters = hti.HersheyFonts()

	fig, ax = plt.subplots()
		
	plt.xlim(-0, 200)
	plt.ylim(0, 200)


	image = Image.open('../pictures/bear_walk.jpg')	
	img_array = outline_path.img_to_bool_array(image, 200)

	bear = outline_path.outline_outer_image(img_array, min_path_length = 5, loading_bar = True)
	bear = pu.scale_all_paths(p2p.paths_to_polys(bear), 100, 100)
	bear = pu.invert_all_paths(bear)
	bear = pu.translate_all_paths(bear, 50, 80)


 

	symbol = letters.arrange_paragraph("This is just a block of text. If I was more creative, I'd write something smart like, \"Keep on plodding along\"", 500)

	symbol = pu.scale_all_paths(symbol, 200, 1000)



	
	symbol = pu.invert_all_paths(symbol)

	symbol += bear

	symbol = pu.translate_all_paths(symbol, 0, 50)

	symbol = pu.scale_all_paths(symbol, 100, 1000)

	pu.plot_paths(symbol, ax)

	plt.show()

	gci.generate_gcode("./g_code_output/bear_and_text", symbol)

