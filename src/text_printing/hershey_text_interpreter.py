import text_printing.bourke_interpreter as bi

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
			
			return (left_pos, right_pos, letter)


	def word_path(self, string):
		NotImplemented





