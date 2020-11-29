import text_printing.bourke_interpreter as bi
import path_utility as pu

class HersheyFonts:

	def __init__(self, path_to_hershey = "./text_printing/hershey/hershey.txt", font = None):


		hershey_font_file = open(path_to_hershey, 'r')
		self.hershey_string_list = hershey_font_file.readlines() 

		self.letter_dict = {}

		if font is None:
			charset = bi.get_encoding()
		else: 
			charset = bi.get_encoding(font)

		for char, line in charset:
			self.letter_dict[char] = self.get_letter(line)


	def get_letter(self, line):

		left_pos = 0;
		right_pos = 0;
		sequence = {}
		letter = []

		#get the line that includes the given line string
		line_string = next(i for i in self.hershey_string_list if line in i)

		#if that line exists:
		if line_string is not None:

			#from the encoding, grab the left and right positions of the letter

			left_pos = ord(line_string[8]) - ord('R')
			right_pos = ord(line_string[9]) - ord('R')


			#iterate through the following string
			verticies = line_string[10:]			
			while len(verticies) > 3:
								
				#" R" encodes a "pen up", so if we see this then we save our current sequence and start a new one
				if (verticies[0:2] == " R"):
					if len(sequence) > 0: letter.append(sequence)
					sequence = {}
				
				elif verticies[2:4] != " R":
					x_coord = ord(verticies[0]) - ord('R')
					y_coord = ord(verticies[1]) - ord('R')

					x1 = ord(verticies[2]) - ord('R')
					y1 = ord(verticies[3]) - ord('R')
					
					sequence[(x_coord, y_coord)] = (x1, y1)		
					
				verticies = verticies[2:]

			if len(sequence) > 0: letter.append(sequence)	
			
			return (left_pos, right_pos, letter)


	def arrange_paragraph(self, string, max_line_length):
		
		paragraph_paths = []

		paragraph = []
		paragraph[:] = string


		cur_x = 0
		index = 0
		len_par = len(paragraph)
		while index < len_par: 

			char = paragraph[index]

			if char == "\n":
				cur_x = 0

			else:	
				start, stop, paths = self.letter_dict[char]
				cur_x += stop-start

				if cur_x > max_line_length:
					i = 0
					while paragraph[index-i] != " " and paragraph[index-i] != "\n":
						i+=1

					if paragraph[index-i] == " ":
						paragraph[index-i] = "\n"

					else:
						paragraph.insert(index-2, "-")
						paragraph.insert(index-1, "\n")
						len_par +=2
					cur_x = 0
					index = index-i

			index +=1


		cur_x = 0
		line = 0

		for char in paragraph:
			if char == "\n":
				cur_x = 0
				line +=1

			else:
				start, stop, paths = self.letter_dict[char]
				paths = pu.translate_all_paths(paths, cur_x-start, line *30)
				cur_x += stop-start
				paragraph_paths += paths
				
		return paragraph_paths




