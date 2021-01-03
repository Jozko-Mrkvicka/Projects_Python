import os
import json
import msvcrt
import copy

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
BTN_F1          = 59
BTN_F5          = 63
BTN_F6          = 64
BTN_ARROW_UP    = 72
BTN_ARROW_DOWN  = 80
BTN_ARROW_RIGHT = 77
BTN_ARROW_LEFT  = 75

gMatrix = []

min_x = 0
min_y = 0
check = "Not checked"

gAvailable_numbers = []
gX = -1
gY = -1

gFinished = False
gStep = 0
gDone = False

###############################################################################
# Initialize whole Sudoku matrix with default values.
# "solved"  - A matrix element has already correct number filled in.
# "checked" - Vertical, horizontal and submatrix checks were already performed
#             from perspective of particular element.
###############################################################################
def matrix_init(matrix):
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
def matrix_print_available_numbers(matrix, x, y):
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
def matrix_print_line(matrix, line, curs_x, curs_y):
	if ((3 == line) or (6 == line)):
		color_print("╠═════════╪═════════╪═════════╬═════════╪═════════╪═════════╬═════════╪═════════╪═════════╣\n");
	elif (0 != line):
		color_print("╟─────────┼─────────┼─────────╫─────────┼─────────┼─────────╫─────────┼─────────┼─────────╢\n");

	color_print("║");    matrix_print_available_numbers(matrix, 0, line);
	color_print("│");    matrix_print_available_numbers(matrix, 1, line);
	color_print("│");    matrix_print_available_numbers(matrix, 2, line);
	color_print("║");    matrix_print_available_numbers(matrix, 3, line);
	color_print("│");    matrix_print_available_numbers(matrix, 4, line);
	color_print("│");    matrix_print_available_numbers(matrix, 5, line);
	color_print("║");    matrix_print_available_numbers(matrix, 6, line);
	color_print("│");    matrix_print_available_numbers(matrix, 7, line);
	color_print("│");    matrix_print_available_numbers(matrix, 8, line);
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
def matrix_print(matrix, curs_x, curs_y):
	color_print("╔═════════╤═════════╤═════════╦═════════╤═════════╤═════════╦═════════╤═════════╤═════════╗\n")

	for y in range(MATRIX_DIM_Y):
		matrix_print_line(matrix, y, curs_x, curs_y)

	color_print("╚═════════╧═════════╧═════════╩═════════╧═════════╧═════════╩═════════╧═════════╧═════════╝\n")
#enddef


###############################################################################
# Draw simple save/load menu.
###############################################################################
def matrix_save_load_menu(matrix, action):
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

	return matrix
#enddef


###############################################################################
# Redraw whole screen.
###############################################################################
def refresh_screen(matrix, curs_x, curs_y):
	os.system("cls")
	color_on(YELLOW)
	print("╔═════════════════════════════════════════════════════════════════════════════════════════╗")
	print("║                                     Sudoku Solver                                       ║")
	print("╚═════════════════════════════════════════════════════════════════════════════════════════╝")
	color_off()

	matrix_print(matrix, curs_x, curs_y)

	color_on(YELLOW)
	print("╔═══════════╦═════════════╦════════════╦═════════════╦══════════════╦══════════╦══════════╗")
	print("║ ESC Exit  ║ DEL Delete  ║ ←↑→↓ Move  ║ 1..9 Value  ║ SPACE Solve  ║ F5 Save  ║ F6 Load  ║")
	print("╚═══════════╩═════════════╩════════════╩═════════════╩══════════════╩══════════╩══════════╝")
	color_off()
	# print("num_of_solved_elements  =", matrix[VARIABLE]['num_of_solved_elements'])
	# print("num_of_checked_elements =", matrix[VARIABLE]['num_of_checked_elements'])
	# print("min_x =", min_x)
	# print("min_y =", min_y)
	# print("check =", check)
	print("gAvailable_numbers =", gAvailable_numbers)
	print("gX =", gX)
	print("gY =", gY)
	print("step =", gStep)
	print("finished =", gFinished)

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


def find_submatrix_limits(curs_x, curs_y):
	if (curs_x in range(0, 3)):
		lim_min_x = 0
		lim_max_x = 3

	elif (curs_x in range(3, 6)):
		lim_min_x = 3
		lim_max_x = 6

	elif (curs_x in range(6, 9)):
		lim_min_x = 6
		lim_max_x = 9


	if (curs_y in range(0, 3)):
		lim_min_y = 0
		lim_max_y = 3

	elif (curs_y in range(3, 6)):
		lim_min_y = 3
		lim_max_y = 6

	elif (curs_y in range(6, 9)):
		lim_min_y = 6
		lim_max_y = 9

	return lim_min_x, lim_max_x, lim_min_y, lim_max_y
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
def remove_known_numbers_from_line(matrix, x, y):
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

	return matrix
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
def remove_known_numbers_from_column(matrix, x, y):
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

	return matrix
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
def remove_known_numbers_from_submatrix(matrix, curs_x, curs_y):
	lim_min_x, lim_max_x, lim_min_y, lim_max_y = find_submatrix_limits(curs_x, curs_y)

	for j in range(lim_min_y, lim_max_y):
		for i in range(lim_min_x, lim_max_x):
			if (matrix[curs_x][curs_y]['solution'] in matrix[i][j]['available_numbers']):
				matrix[i][j]['available_numbers'].remove(matrix[curs_x][curs_y]['solution'])
			#endif

			if (1 == len(matrix[i][j]['available_numbers'])):
				matrix[i][j]['solved'] = True
				matrix[i][j]['solution'] = matrix[i][j]['available_numbers'][0]
				matrix[i][j]['available_numbers'].pop(0)
				matrix[VARIABLE]['num_of_solved_elements'] = matrix[VARIABLE]['num_of_solved_elements'] + 1
			#endif
		#endfor
	#endfor

	return matrix
#enddef


###############################################################################
# Add new value to matrix or overwrite old one.
###############################################################################
def add_value(matrix, curs_x, curs_y, value):
	# Increment counter only if element is still empty.
	if (False == matrix[curs_x][curs_y]['solved']):
		matrix[VARIABLE]['num_of_solved_elements'] = matrix[VARIABLE]['num_of_solved_elements'] + 1

	matrix[curs_x][curs_y]['solution'] = value
	matrix[curs_x][curs_y]['solved'] = True
	matrix[curs_x][curs_y]['available_numbers'] = []

	return matrix
#enddef


###############################################################################
# Delete value from matrix.
###############################################################################
def delete_value(matrix, curs_x, curs_y):
	# Decrement counter only if element has still some value.
	if (True == matrix[curs_x][curs_y]['solved']):
		matrix[VARIABLE]['num_of_solved_elements'] = matrix[VARIABLE]['num_of_solved_elements'] - 1
		# matrix[VARIABLE]['num_of_checked_elements'] = matrix[VARIABLE]['num_of_checked_elements'] - 1
		matrix[curs_x][curs_y]['solved'] = False
		matrix[curs_x][curs_y]['available_numbers'] = [matrix[curs_x][curs_y]['solution']] #[1, 2, 3, 4, 5, 6, 7, 8, 9]
		matrix[curs_x][curs_y]['solution'] = EMPTY
	#endif

	return matrix
	# TODO: pridat naspat vymazane cislo do riadkov, stlpcov a submatrixu
#enddef


def verify_line(matrix, line):
	numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	for i in range(MATRIX_DIM_X):
		if matrix[i][line]['solution'] in numbers:
			numbers.remove(matrix[i][line]['solution'])

	if (0 == len(numbers)):
		return True
	else:
		return False
#enddef


def verify_column(matrix, column):
	numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	for i in range(MATRIX_DIM_Y):
		if matrix[column][i]['solution'] in numbers:
			numbers.remove(matrix[column][i]['solution'])

	if (0 == len(numbers)):
		return True
	else:
		return False
#enddef


def verify_submatrix(matrix, curs_x, curs_y):
	lim_min_x, lim_max_x, lim_min_y, lim_max_y = find_submatrix_limits(curs_x, curs_y)

	numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	for y in range(lim_min_y, lim_max_y):
		for x in range(lim_min_x, lim_max_x):
			if matrix[x][y]['solution'] in numbers:
				numbers.remove(matrix[x][y]['solution'])

	if (0 == len(numbers)):
		return True
	else:
		return False
#enddef


def is_matrix_solved(matrix):
	for i in range(MATRIX_DIM_Y):
		if (False == verify_line(matrix, i)):
			return False
		#endif
	#endfor

	for i in range(MATRIX_DIM_X):
		if (False == verify_column(matrix, i)):
			return False
		#endif
	#endfor

	for y in [0, 3, 6]:
		for x in [0, 3, 6]:
			if (False == verify_submatrix(matrix, x, y)):
				return False
			#endif
		#endfor
	#endfor

	return True
#enddef


def is_matrix_filled(matrix):
	for x in range(MATRIX_DIM_X):
		for y in range(MATRIX_DIM_Y):
			if (False == matrix[x][y]["solved"]):
				return False
			#endif
		#endfor
	#endfor

	return True
#enddef


def remove_known_numbers(matrix):
	while ((matrix[VARIABLE]['num_of_checked_elements'] != matrix[VARIABLE]['num_of_solved_elements']) and (0 != matrix[VARIABLE]['num_of_solved_elements'])):
		for x in range(MATRIX_DIM_X):
			for y in range(MATRIX_DIM_Y):
				if ((True == matrix[x][y]['solved']) and (False == matrix[x][y]['checked'])):
					matrix = remove_known_numbers_from_line(matrix, x, y)
					matrix = remove_known_numbers_from_column(matrix, x, y)
					matrix = remove_known_numbers_from_submatrix(matrix, x, y)
					matrix[x][y]['checked'] = True
					matrix[VARIABLE]['num_of_checked_elements'] = matrix[VARIABLE]['num_of_checked_elements'] + 1
				#endif
			#endfor
		#endfor
	#endwhile

	return matrix
#enddef


# Go through whole matrix and find first element with the lowest count of available numbers.
def find_unsolved_element(matrix):
	global min_x
	global min_y

	min_cnt_of_available_numbers = 10
	available_numbers = []
	min_x = -1
	min_y = -1
	for x in range(MATRIX_DIM_X):
		for y in range(MATRIX_DIM_Y):
			if (False == matrix[x][y]['solved']) and (len(matrix[x][y]['available_numbers']) < min_cnt_of_available_numbers):
				min_cnt_of_available_numbers = len(matrix[x][y]['available_numbers'])
				available_numbers.clear()
				available_numbers.extend(matrix[x][y]['available_numbers'])
				min_x = x
				min_y = y
			#endif
		#endfor
	#endfor

	return min_x, min_y, available_numbers
#enddef


###############################################################################
# Solve the matrix.
###############################################################################
def matrix_solve(matrix, x, y, number_to_try):
	# global gDone
	global gStep
	global gAvailable_numbers
	global gX
	global gY

	gStep = gStep + 1

	temp_matrix = copy.deepcopy(matrix)

	temp_matrix[x][y]['solved'] = True
	temp_matrix[x][y]['solution'] = number_to_try
	temp_matrix[x][y]['available_numbers'] = []
	temp_matrix[VARIABLE]['num_of_solved_elements'] = temp_matrix[VARIABLE]['num_of_solved_elements'] + 1

	temp_matrix = remove_known_numbers(temp_matrix)

	if (True == is_matrix_filled(temp_matrix)):
		refresh_screen(temp_matrix, 0, 0)
		if (True == is_matrix_solved(temp_matrix)):
			print("Sudoku is solved!!")
			return True
		else:
			print("Whole matrix is filled with numbers but it does not pass the checks. We have incorrect solution.")
			return False
		#endif
	#endif

	if (False == is_matrix_filled(temp_matrix)):
		x, y, available_numbers = find_unsolved_element(temp_matrix)
		gAvailable_numbers = available_numbers
		gX = x
		gY = y

		refresh_screen(temp_matrix, 0, 0)
		# input()

		done = False
		for i in range(len(available_numbers)):
			# if (False == gDone):
			done = matrix_solve(temp_matrix, x, y, available_numbers[i])
			if (True == done):
				return True
		#endfor
	#endif

#enddef


def main():
	global gMatrix
	global finished

	cursor("off")
	os.system('')
	curs_x = 0
	curs_y = 0
	matrix_init(gMatrix)

	g = "0"
	while (ord(g) != BTN_ESC):
		refresh_screen(gMatrix, curs_x, curs_y)
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
			gMatrix = add_value(gMatrix, curs_x, curs_y, int(g))

		if (BTN_DELETE == ord(g)):
			gMatrix = delete_value(gMatrix, curs_x, curs_y)

		# TODO: New game

		if (BTN_F1 == ord(g)):
			if (True == is_matrix_solved(gMatrix)):
				finished = True

		if (BTN_F5 == ord(g)):
			matrix_save_load_menu(gMatrix, "Save")

		if (BTN_F6 == ord(g)):
			gMatrix = matrix_save_load_menu(gMatrix, "Load")

		if (BTN_SPACE == ord(g)):
			remove_known_numbers(gMatrix)

			if (True == is_matrix_filled(gMatrix)):
				if (True == is_matrix_solved(gMatrix)):
					print("Sudoku is solved!! No recursion needed.")
				else:
					print("Whole matrix is filled with numbers but it does not pass the checks. We have incorrect solution.")
				#endif
			#endif

			if (False == is_matrix_filled(gMatrix)):
				x, y, available_numbers = find_unsolved_element(gMatrix)

				done = False
				for i in range(len(available_numbers)):
					done = matrix_solve(gMatrix, x, y, available_numbers[i])
					if (True == done):
						return True
				#endfor
			#endif
		#endif

	#endwhile

	cursor("on")
#enddef


main()

# status = []
# status.append \
# (
# 	{
# 		"matrix":""
# 	}
# )

# status[0] = {}

# print(status)

# 0 ulozim stav
# 1 najdem element s najmensim poctom moznosti a vyberiem si jednu
# 2 riesim kym sa da
# 3 skontrolujem ze nemam jedno cislo dvakrat
#	3a ak detekujem chybu (jedno cislo viackrat) tak
# 		nacitam ulozeny stav (krok 0)
# 		vratim sa na krok 1 (vyberiem ine cislo)
# 4 skontrolujem ci uz mam kompletne riesenie
# 5 opakujem krok 1

# g = '0'
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
