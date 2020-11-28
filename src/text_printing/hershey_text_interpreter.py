class HersheyFonts:

	def __init__(self, path_to_hershey, charset = None):

		hershey_font_file = open(path_to_hershey, 'r')
		self.hershey_string_list = hershey_font_file.readlines() 

		self.letter_dict = {}

		charset = []

		for index, letter in enumerate(" abcdefghijklmnopqrstuvwxyz"):
			if index >0:
				padding = " " * (4-len(str(index)))
				charset.append((letter, padding + str(index)))

		for char, line in charset:
			self.get_letter(char, line)


	def get_letter(self, symbol, line):

		left_pos = 0;
		right_pos = 0;
		sequence = {}
		letter = []

		line_string = next(i for i in self.hershey_string_list if line in i)

		if line_string is not None:

			verticies = int(line_string[5:8])
		
			left_pos = ord(line_string[8]) - ord('R')
			right_pos = ord(line_string[9]) - ord('R')

			verticies = line_string[10:]
			
			while len(verticies) > 3:
								
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

			letter.append(sequence)		
			

			self.letter_dict[symbol] = (left_pos, right_pos, letter)


	def word_path(self, string):
		NotImplemented





