
#http://paulbourke.net/dataformats/hershey/italict.hmp

def get_encoding(burke_file = "./text_printing/hershey/bourke.txt"):

	with open(burke_file, "r") as file:
		list_of_indexes = file.read().replace('\n', ' ')

	pairs = []
	lines = 0

	for char_ascii in range(32, 126):
		#scrub any spaces
		while list_of_indexes[0:1] == " ": list_of_indexes = list_of_indexes[1:]
		
		end_index = list_of_indexes.index(" ")

		char_index = list_of_indexes[:end_index]

		if "-" in char_index:
			first_num = char_index[:char_index.index("-")]
			second_num = char_index[char_index.index("-")+1:]

			char_index = first_num
			
			list_of_indexes = (" ".join(map(str, range(int(first_num)+1,int(second_num)+1)))) + list_of_indexes[end_index:]

		else:
			list_of_indexes = list_of_indexes[end_index:]

		#print(list_of_indexes)
		padded_char_index_string = " " * (4-len(str(char_index))) + str(char_index)
		pairs.append((chr(char_ascii), padded_char_index_string))

	return (pairs)

	
