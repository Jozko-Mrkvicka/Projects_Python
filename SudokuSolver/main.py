import os
import json
import msvcrt

# Colors
DEFAULT = 0
BRIGHT  = 1
RED     = 31
YELLOW  = 93

MATRIX_DIM_X = 9
MATRIX_DIM_Y = 9
VARIABLE     = 9
NUM_OF_FILES = 6
DEBUG        = False
EMPTY        = " "

BTN_ESC         = 27
BTN_ENTER       = 13
BTN_SPACE       = 32
BTN_DELETE      = 83
BTN_F5          = 63
BTN_F6          = 64
BTN_ARROW_UP    = 72
BTN_ARROW_DOWN  = 80
BTN_ARROW_RIGHT = 77
BTN_ARROW_LEFT  = 75


matrix = []

###############################################################################
# Initialize whole Sudoku matrix with default values.
# "solved"  - A matrix element has already correct number filled in.
# "checked" - Vertical, horizontal and submatrix checks were already performed
#             from perspective of particular element.
###############################################################################
def matrix_init():
	for x in range(MATRIX_DIM_X):
		matrix.append([])

		for y in range(MATRIX_DIM_Y):
			matrix[x].append(y)
			matrix[x][y] = \
			{
				"index"             : (x + 1)*10 + (y + 1),
				"solved"            : False,
				"checked"           : False,
				"available_numbers" : [1, 2, 3, 4, 5, 6, 7, 8, 9],
				"solution"          : EMPTY
			}
		#endfor
	#endfor

	matrix.append([])
	matrix[VARIABLE] = \
	{
		"num_of_solved_elements"  : 0,
		"num_of_checked_elements" : 0
	}
#enddef


###############################################################################
# This function prints all of the numbers which are still possible to be placed
# in an element.
###############################################################################
def matrix_print_available_numbers(x,y):
	count = len(matrix[x][y]["available_numbers"])
	for i in range(count):
		print(matrix[x][y]["available_numbers"][i], end = '')
	#endfor

	# Print remaining spaces
	for i in range(9 - count):
		print(" ", end = '')
	#endfor
#enddef


###############################################################################
# Set text color
###############################################################################
def color_on(color):
	print("\033[" + str(color) + "m", end = '')
#enddef


###############################################################################
# Clear text color
###############################################################################
def color_off():
	print("\033[" + str(DEFAULT) + "m", end = '')
#enddef


###############################################################################
# Print characters with specific color.
###############################################################################
def color_print(str):
	color = DEFAULT
	for i in str:
		if i in ['═', '║', '╬', '╠', '╣', '╦', '╩', '╔', '╗', '╚', '╝', '╫', '╪', '╟', '╢', '╤', '╧', "-", ">", "<"]:
			color = YELLOW

		elif i in ['─', '┼', '│']:
			color = DEFAULT

		else:
			color = DEFAULT

		color_on(color)
		print(i, end = '')
		color_off()
	#endfor
#enddef


###############################################################################
# Print one line of Sudoku matrix.
###############################################################################
def matrix_print_line(line, curs_x, curs_y):
	if ((3 == line) or (6 == line)):
		color_print("╠═════════╪═════════╪═════════╬═════════╪═════════╪═════════╬═════════╪═════════╪═════════╣\n");
	elif (0 != line):
		color_print("╟─────────┼─────────┼─────────╫─────────┼─────────┼─────────╫─────────┼─────────┼─────────╢\n");

	color_print("║");    matrix_print_available_numbers(0, line);
	color_print("│");    matrix_print_available_numbers(1, line);
	color_print("│");    matrix_print_available_numbers(2, line);
	color_print("║");    matrix_print_available_numbers(3, line);
	color_print("│");    matrix_print_available_numbers(4, line);
	color_print("│");    matrix_print_available_numbers(5, line);
	color_print("║");    matrix_print_available_numbers(6, line);
	color_print("│");    matrix_print_available_numbers(7, line);
	color_print("│");    matrix_print_available_numbers(8, line);
	color_print("║\n");

	color_print("╟─────────┼─────────┼─────────╫─────────┼─────────┼─────────╫─────────┼─────────┼─────────╢\n")

	color_print("║");    color_print(matrix[0][line]["index"], "      ") if (True == DEBUG) else color_print("         ");
	color_print("│");    color_print(matrix[1][line]["index"], "      ") if (True == DEBUG) else color_print("         ");
	color_print("│");    color_print(matrix[2][line]["index"], "      ") if (True == DEBUG) else color_print("         ");
	color_print("║");    color_print(matrix[3][line]["index"], "      ") if (True == DEBUG) else color_print("         ");
	color_print("│");    color_print(matrix[4][line]["index"], "      ") if (True == DEBUG) else color_print("         ");
	color_print("│");    color_print(matrix[5][line]["index"], "      ") if (True == DEBUG) else color_print("         ");
	color_print("║");    color_print(matrix[6][line]["index"], "      ") if (True == DEBUG) else color_print("         ");
	color_print("│");    color_print(matrix[7][line]["index"], "      ") if (True == DEBUG) else color_print("         ");
	color_print("│");    color_print(matrix[8][line]["index"], "      ") if (True == DEBUG) else color_print("         ");
	color_print("║\n");

	color_print("║");    color_print("    " + str(matrix[0][line]["solution"]) + "    ")
	color_print("│");    color_print("    " + str(matrix[1][line]["solution"]) + "    ")
	color_print("│");    color_print("    " + str(matrix[2][line]["solution"]) + "    ")
	color_print("║");    color_print("    " + str(matrix[3][line]["solution"]) + "    ")
	color_print("│");    color_print("    " + str(matrix[4][line]["solution"]) + "    ")
	color_print("│");    color_print("    " + str(matrix[5][line]["solution"]) + "    ")
	color_print("║");    color_print("    " + str(matrix[6][line]["solution"]) + "    ")
	color_print("│");    color_print("    " + str(matrix[7][line]["solution"]) + "    ")
	color_print("│");    color_print("    " + str(matrix[8][line]["solution"]) + "    ")
	color_print("║\n");

	if (curs_y != line):     color_print("║         │         │         ║         │         │         ║         │         │         ║\n")
	elif (0 == curs_x):      color_print("║ --> <-- │         │         ║         │         │         ║         │         │         ║\n")
	elif (1 == curs_x):      color_print("║         │ --> <-- │         ║         │         │         ║         │         │         ║\n")
	elif (2 == curs_x):      color_print("║         │         │ --> <-- ║         │         │         ║         │         │         ║\n")
	elif (3 == curs_x):      color_print("║         │         │         ║ --> <-- │         │         ║         │         │         ║\n")
	elif (4 == curs_x):      color_print("║         │         │         ║         │ --> <-- │         ║         │         │         ║\n")
	elif (5 == curs_x):      color_print("║         │         │         ║         │         │ --> <-- ║         │         │         ║\n")
	elif (6 == curs_x):      color_print("║         │         │         ║         │         │         ║ --> <-- │         │         ║\n")
	elif (7 == curs_x):      color_print("║         │         │         ║         │         │         ║         │ --> <-- │         ║\n")
	elif (8 == curs_x):      color_print("║         │         │         ║         │         │         ║         │         │ --> <-- ║\n")
#enddef


###############################################################################
# Print whole Sudoku matrix.
###############################################################################
def matrix_print(curs_x, curs_y):
	color_print("╔═════════╤═════════╤═════════╦═════════╤═════════╤═════════╦═════════╤═════════╤═════════╗\n")

	for y in range(MATRIX_DIM_Y):
		matrix_print_line(y, curs_x, curs_y)

	color_print("╚═════════╧═════════╧═════════╩═════════╧═════════╧═════════╩═════════╧═════════╧═════════╝\n")
#enddef


###############################################################################
# Draw simple save/load menu.
###############################################################################
def matrix_save_load_menu(action):
	global matrix

	file_list = []
	i = 0
	for file in range(NUM_OF_FILES):
		i = i + 1
		file_list.append("save" + str(i) + ".json")

	curs_y = 0
	g = "0"
	while ((BTN_ESC != ord(g)) and (BTN_ENTER != ord(g))):
		os.system('cls')
		print("╔═════════════════╗")
		print("║    " + action + " Game    ║")
		print("╠═════════════════╣")

		i = 0
		for file in file_list:
			if (curs_y == i):
				print("║ -> ", file, " ║")
			else:
				print("║    ", file, " ║")
			i = i + 1
		#endfor

		print("╚═════════════════╝")

		g = msvcrt.getch()

		if (BTN_ARROW_UP    == ord(g)):
			curs_y = curs_y - 1

		if (BTN_ARROW_DOWN  == ord(g)):
			curs_y = curs_y + 1

		if (NUM_OF_FILES == curs_y):
			curs_y = 0

		if (-1 == curs_y):
			curs_y = NUM_OF_FILES - 1

		if (BTN_ENTER == ord(g)):
			if (action == "Load"):
				with open(file_list[curs_y], 'r') as json_file:
					matrix = json.load(json_file)

			if (action == "Save"):
				with open(file_list[curs_y], 'w') as json_file:
					json.dump(matrix, json_file, indent=4)
		#endif
	#endwhile
#enddef


###############################################################################
# Redraw whole screen.
###############################################################################
def refresh_screen(curs_x, curs_y):
	os.system("cls")
	color_on(YELLOW)
	print("╔═════════════════════════════════════════════════════════════════════════════════════════╗")
	print("║                                     Sudoku Solver                                       ║")
	print("╚═════════════════════════════════════════════════════════════════════════════════════════╝")
	color_off()

	matrix_print(curs_x, curs_y)

	color_on(YELLOW)
	print("╔═══════════╦═════════════╦════════════╦═════════════╦══════════════╦══════════╦══════════╗")
	print("║ ESC Exit  ║ DEL Delete  ║ ←↑→↓ Move  ║ 1..9 Value  ║ SPACE Solve  ║ F5 Save  ║ F6 Load  ║")
	print("╚═══════════╩═════════════╩════════════╩═════════════╩══════════════╩══════════╩══════════╝")
	color_off()
	print("num_of_solved_elements  =", matrix[VARIABLE]['num_of_solved_elements'])
	print("num_of_checked_elements =", matrix[VARIABLE]['num_of_checked_elements'])
#enddef


###############################################################################
# Switch on/off cursor.
###############################################################################
def cursor(option):
	if ("on" == option):
		print("\033[?25h", end = '')

	if ("off" == option):
		print("\033[?25l", end = '')
#enddef


###############################################################################
# Input: Coordinates of one matrix element.
# This function goes through whole line and it deletes already known element
# numbers from all lists of available numbers which exists in particular line
# (because the same number can`t exist in multiple elements of the same line
# in Sudoku).
# If there is only one available number left in an element then the element
# is claimed to be solved.
###############################################################################
def check_line(x, y):
	for i in range(MATRIX_DIM_X):
		if (matrix[x][y]['solution'] in matrix[i][y]['available_numbers']):
			matrix[i][y]['available_numbers'].remove(matrix[x][y]['solution'])
		#endif

		if (1 == len(matrix[i][y]['available_numbers'])):
			matrix[i][y]['solved'] = True
			matrix[i][y]['solution'] = matrix[i][y]['available_numbers'][0]
			matrix[i][y]['available_numbers'].pop(0)
			matrix[VARIABLE]['num_of_solved_elements'] = matrix[VARIABLE]['num_of_solved_elements'] + 1
		#endif
	#endfor
#enddef


###############################################################################
# Input: Coordinates of one matrix element.
# This function goes through whole column and it deletes already known element
# numbers from all lists of available numbers which exists in particular column
# (because the same number can`t exist in multiple elements of the same column
# in Sudoku).
# If there is only one available number left in an element then the element
# is claimed to be solved.
###############################################################################
def check_column(x, y):
	for i in range(MATRIX_DIM_Y):
		if (matrix[x][y]['solution'] in matrix[x][i]['available_numbers']):
			matrix[x][i]['available_numbers'].remove(matrix[x][y]['solution'])
		#endif

		if (1 == len(matrix[x][i]['available_numbers'])):
			matrix[x][i]['solved'] = True
			matrix[x][i]['solution'] = matrix[x][i]['available_numbers'][0]
			matrix[x][i]['available_numbers'].pop(0)
			matrix[VARIABLE]['num_of_solved_elements'] = matrix[VARIABLE]['num_of_solved_elements'] + 1
		#endif
	#endfor
#enddef


###############################################################################
# Input: Coordinates of one matrix element.
# This function goes through whole submatrix (3x3) and it deletes already known
# element numbers from all lists of available numbers which exists in particular
# submatrix (because the same number can`t exist in multiple elements of the same
# submatrix in Sudoku).
# If there is only one available number left in an element then the element
# is claimed to be solved.
###############################################################################
def check_submatrix(x, y):
	if (x in range(0, 3)):
		lim_min_x = 0
		lim_max_x = 3

	elif (x in range(3, 6)):
		lim_min_x = 3
		lim_max_x = 6

	elif (x in range(6, 9)):
		lim_min_x = 6
		lim_max_x = 9


	if (y in range(0, 3)):
		lim_min_y = 0
		lim_max_y = 3

	elif (y in range(3, 6)):
		lim_min_y = 3
		lim_max_y = 6

	elif (y in range(6, 9)):
		lim_min_y = 6
		lim_max_y = 9

	for j in range(lim_min_y, lim_max_y):
		for i in range(lim_min_x, lim_max_x):
			if (matrix[x][y]['solution'] in matrix[i][j]['available_numbers']):
				matrix[i][j]['available_numbers'].remove(matrix[x][y]['solution'])
			#endif

			if (1 == len(matrix[i][j]['available_numbers'])):
				matrix[i][j]['solved'] = True
				matrix[i][j]['solution'] = matrix[i][j]['available_numbers'][0]
				matrix[i][j]['available_numbers'].pop(0)
				matrix[VARIABLE]['num_of_solved_elements'] = matrix[VARIABLE]['num_of_solved_elements'] + 1
			#endif
		#endfor
	#endfor
#enddef


###############################################################################
# Add new value to matrix or overwrite old one.
###############################################################################
def add_value(curs_x, curs_y, value):
	# Increment counter only if element is still empty.
	if (False == matrix[curs_x][curs_y]['solved']):
		matrix[VARIABLE]['num_of_solved_elements'] = matrix[VARIABLE]['num_of_solved_elements'] + 1

	matrix[curs_x][curs_y]['solution'] = value
	matrix[curs_x][curs_y]['solved'] = True
	matrix[curs_x][curs_y]['available_numbers'] = []
#enddef


###############################################################################
# Delete value from matrix.
###############################################################################
def delete_value(curs_x, curs_y):
	# Decrement counter only if element has still some value.
	if (True == matrix[curs_x][curs_y]['solved']):
		matrix[VARIABLE]['num_of_solved_elements'] = matrix[VARIABLE]['num_of_solved_elements'] - 1
		# matrix[VARIABLE]['num_of_checked_elements'] = matrix[VARIABLE]['num_of_checked_elements'] - 1
		matrix[curs_x][curs_y]['solved'] = False
		matrix[curs_x][curs_y]['available_numbers'] = [matrix[curs_x][curs_y]['solution']] #[1, 2, 3, 4, 5, 6, 7, 8, 9]
		matrix[curs_x][curs_y]['solution'] = EMPTY

	# TODO: pridat naspat vymazane cislo do riadkov, stlpcov a submatrixu
#enddef


###############################################################################
# Solve the matrix.
###############################################################################
def matrix_solve():
	while ((matrix[VARIABLE]['num_of_checked_elements'] != matrix[VARIABLE]['num_of_solved_elements']) and (0 != matrix[VARIABLE]['num_of_solved_elements'])):
		for x in range(MATRIX_DIM_X):
			for y in range(MATRIX_DIM_Y):
				if ((True == matrix[x][y]['solved']) and (False == matrix[x][y]['checked'])):
					check_line(x, y)
					check_column(x, y)
					check_submatrix(x, y)
					matrix[x][y]['checked'] = True
					matrix[VARIABLE]['num_of_checked_elements'] = matrix[VARIABLE]['num_of_checked_elements'] + 1
				#endif
			#endfor
		#endfor
	#endwhile
#enddef


def main():
	global matrix

	cursor("off")
	os.system('')
	curs_x = 0
	curs_y = 0
	matrix_init()

	g = "0"
	while (ord(g) != BTN_ESC):
		refresh_screen(curs_x, curs_y)
		g = msvcrt.getch()

		if (BTN_ARROW_UP    == ord(g)):
			curs_y = curs_y - 1
			if (curs_y < 0):
				curs_y = 8

		if (BTN_ARROW_DOWN  == ord(g)):
			curs_y = curs_y + 1
			if (curs_y > 8):
				curs_y = 0

		if (BTN_ARROW_RIGHT == ord(g)):
			curs_x = curs_x + 1
			if (curs_x > 8):
				curs_x = 0

		if (BTN_ARROW_LEFT  == ord(g)):
			curs_x = curs_x - 1
			if (curs_x < 0):
				curs_x = 8

		if ((ord(g) - ord('0')) in [1, 2, 3, 4, 5, 6, 7, 8, 9]):
			add_value(curs_x, curs_y, int(g))

		if (BTN_DELETE == ord(g)):
			delete_value(curs_x, curs_y)

		if (BTN_F5 == ord(g)):
			matrix_save_load_menu("Save")

		if (BTN_F6 == ord(g)):
			matrix_save_load_menu("Load")

		if (BTN_SPACE == ord(g)):
			matrix_solve()
	#endwhile

	cursor("on")
#enddef


main()


# 0 ulozim stav
# 1 najdem element s najmensim poctom moznosti a vyberiem si jednu
# 2 riesim kym sa da
# 3 skontrolujem ze nemam jedno cislo dvakrat
#	3a ak detekujem chybu (jedno cislo viackrat) tak
# 		nacitam ulozeny stav (krok 0)
# 		vratim sa na krok 1 (vyberiem ine cislo)
# 4 skontrolujem ci uz mam kompletne riesenie
# 5 opakujem krok 1

# while (ord(g) != 27):
# 	g = msvcrt.getch()
# 	print(ord(g))

# system('')

# print("\N{91}")
# print('\x1b[41m' + 'Test')
# # color_on()
# print("ahoj")
# print("ahoj")
# print("ahoj")
# # color_off()
# # print("\033[5;5H")
# print("\033[A", end = '')
# print("\033[A", end = '')
# print("\033[C", end = '')
# print("\033[C", end = '')
# print("nazdar")

# for i in range(0x2500, 0x2580):
# 	print(i, " = ", chr(i), "   ", end = "\n")


# ─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ┌ ┍ ┎ ┏
# ┐ ┑ ┒ ┓ └ ┕ ┖ ┗ ┘ ┙ ┚ ┛ ├ ┝ ┞ ┟
# ┠ ┡ ┢ ┣ ┤ ┥ ┦ ┧ ┨ ┩ ┪ ┫ ┬ ┭ ┮ ┯
# ┰ ┱ ┲ ┳ ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻ ┼ ┽ ┾ ┿
# ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍ ╎ ╏
# ═ ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙ ╚ ╛ ╜ ╝ ╞ ╟
# ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬ 

# ╔═══════╤══════╦════════╤═══════╗
# ║       │      ║        │       ║
# ╟───────┼──────╫────────┼───────╢
# ║       │      ║        │       ║
# ╠═══════╪══════╬════════╪═══════╣
# ║       │      ║        │       ║
# ║       │      ║        │       ║
# ║       │      ║        │       ║
# ╚═══════╧══════╩════════╧═══════╝

# ┌─┬─┐
# │ │ │
# ├─┼─┤
# │ │ │
# └─┴─┘

# ╔═╦═╗
# ║ ║ ║
# ╠═╬═╣
# ║ ║ ║
# ╚═╩═╝
