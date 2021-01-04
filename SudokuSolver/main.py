###############################################################################
#                              Sudoku Solver
###############################################################################
import os
import json
import msvcrt
import copy

DEFAULT = 0
BRIGHT  = 1
RED     = 31
YELLOW  = 93

MATRIX_DIM_X = 9
MATRIX_DIM_Y = 9
VARIABLE     = 9
NUM_OF_FILES = 6
EMPTY        = " "

BTN_ESC    = 27
BTN_ENTER  = 13
BTN_SPACE  = 32
BTN_DELETE = 83
BTN_F1     = 59
BTN_F5     = 63
BTN_F6     = 64
BTN_UP     = 72
BTN_DOWN   = 80
BTN_RIGHT  = 77
BTN_LEFT   = 75

gMatrix = []
gStep = 0
gMessage = ""

###############################################################################
# Initialize whole Sudoku matrix with default values.
# "solved"  - A matrix element has already correct number filled in.
# "checked" - Vertical, horizontal and submatrix checks were already performed
#             from perspective of particular element.
###############################################################################
def matrix_init(matrix):
	matrix.clear()

	for x in range(MATRIX_DIM_X):
		matrix.append([])

		for y in range(MATRIX_DIM_Y):
			matrix[x].append(y)
			matrix[x][y] = \
			{
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
		#endif

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
		color_print("   ╠═════════╪═════════╪═════════╬═════════╪═════════╪═════════╬═════════╪═════════╪═════════╣\n");
	elif (0 != line):
		color_print("   ╟─────────┼─────────┼─────────╫─────────┼─────────┼─────────╫─────────┼─────────┼─────────╢\n");
	#endif

	color_print("   ║");    matrix_print_available_numbers(matrix, 0, line);
	color_print("│");       matrix_print_available_numbers(matrix, 1, line);
	color_print("│");       matrix_print_available_numbers(matrix, 2, line);
	color_print("║");       matrix_print_available_numbers(matrix, 3, line);
	color_print("│");       matrix_print_available_numbers(matrix, 4, line);
	color_print("│");       matrix_print_available_numbers(matrix, 5, line);
	color_print("║");       matrix_print_available_numbers(matrix, 6, line);
	color_print("│");       matrix_print_available_numbers(matrix, 7, line);
	color_print("│");       matrix_print_available_numbers(matrix, 8, line);
	color_print("║\n");

	color_print("   ╟─────────┼─────────┼─────────╫─────────┼─────────┼─────────╫─────────┼─────────┼─────────╢\n")
	color_print("   ║         │         │         ║         │         │         ║         │         │         ║\n");

	color_print("   ║");    color_print("    " + str(matrix[0][line]["solution"]) + "    ")
	color_print("│");       color_print("    " + str(matrix[1][line]["solution"]) + "    ")
	color_print("│");       color_print("    " + str(matrix[2][line]["solution"]) + "    ")
	color_print("║");       color_print("    " + str(matrix[3][line]["solution"]) + "    ")
	color_print("│");       color_print("    " + str(matrix[4][line]["solution"]) + "    ")
	color_print("│");       color_print("    " + str(matrix[5][line]["solution"]) + "    ")
	color_print("║");       color_print("    " + str(matrix[6][line]["solution"]) + "    ")
	color_print("│");       color_print("    " + str(matrix[7][line]["solution"]) + "    ")
	color_print("│");       color_print("    " + str(matrix[8][line]["solution"]) + "    ")
	color_print("║\n");

	if (curs_y != line):    color_print("   ║         │         │         ║         │         │         ║         │         │         ║\n")
	elif (0 == curs_x):     color_print("   ║ --> <-- │         │         ║         │         │         ║         │         │         ║\n")
	elif (1 == curs_x):     color_print("   ║         │ --> <-- │         ║         │         │         ║         │         │         ║\n")
	elif (2 == curs_x):     color_print("   ║         │         │ --> <-- ║         │         │         ║         │         │         ║\n")
	elif (3 == curs_x):     color_print("   ║         │         │         ║ --> <-- │         │         ║         │         │         ║\n")
	elif (4 == curs_x):     color_print("   ║         │         │         ║         │ --> <-- │         ║         │         │         ║\n")
	elif (5 == curs_x):     color_print("   ║         │         │         ║         │         │ --> <-- ║         │         │         ║\n")
	elif (6 == curs_x):     color_print("   ║         │         │         ║         │         │         ║ --> <-- │         │         ║\n")
	elif (7 == curs_x):     color_print("   ║         │         │         ║         │         │         ║         │ --> <-- │         ║\n")
	elif (8 == curs_x):     color_print("   ║         │         │         ║         │         │         ║         │         │ --> <-- ║\n")
	#endif
#enddef


###############################################################################
# Print whole Sudoku matrix.
###############################################################################
def matrix_print(matrix, curs_x, curs_y):
	color_print("   ╔═════════╤═════════╤═════════╦═════════╤═════════╤═════════╦═════════╤═════════╤═════════╗\n")

	for y in range(MATRIX_DIM_Y):
		matrix_print_line(matrix, y, curs_x, curs_y)
	#endfor

	color_print("   ╚═════════╧═════════╧═════════╩═════════╧═════════╧═════════╩═════════╧═════════╧═════════╝\n")
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
	#endfor

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
			#endif
			i = i + 1
		#endfor

		print("╚═════════════════╝")

		g = msvcrt.getch()

		if (BTN_UP    == ord(g)):
			curs_y = curs_y - 1
		#endif

		if (BTN_DOWN  == ord(g)):
			curs_y = curs_y + 1
		#endif

		if (NUM_OF_FILES == curs_y):
			curs_y = 0
		#endif

		if (-1 == curs_y):
			curs_y = NUM_OF_FILES - 1
		#endif

		if (BTN_ENTER == ord(g)):
			if (action == "Load"):
				with open(file_list[curs_y], 'r') as json_file:
					matrix = json.load(json_file)
				#endwith
			#endif

			if (action == "Save"):
				with open(file_list[curs_y], 'w') as json_file:
					json.dump(matrix, json_file, indent=4)
				#endwith
			#endif
		#endif
	#endwhile

	return matrix
#enddef


###############################################################################
# Redraw whole screen.
###############################################################################
def refresh_screen(matrix, curs_x, curs_y):
	global gMessage
	global gStep

	os.system("cls")
	color_on(YELLOW)
	print("   ╔═════════════════════════════════════════════════════════════════════════════════════════╗")
	print("   ║                                     Sudoku Solver                                       ║")
	print("   ╚═════════════════════════════════════════════════════════════════════════════════════════╝")
	color_off()

	matrix_print(matrix, curs_x, curs_y)

	color_on(YELLOW)
	print("╔══════════╦═════════════╦═════════╦═════════╦════════════╦═══════════╦════════════╦═════════════╗")
	print("║ ESC Exit ║ F1 New Game ║ F5 Save ║ F6 Load ║ DEL Delete ║ ←↑→↓ Move ║ 1..9 Value ║ SPACE Solve ║")
	print("╚══════════╩═════════════╩═════════╩═════════╩════════════╩═══════════╩════════════╩═════════════╝")
	color_off()
	print("step =", gStep)
	print(gMessage)
#enddef


###############################################################################
# Switch on/off cursor.
###############################################################################
def cursor(option):
	if ("on" == option):
		print("\033[?25h", end = '')
	#endif

	if ("off" == option):
		print("\033[?25l", end = '')
	#endif
#enddef


###############################################################################
# Returns minimal and maximal coordinates for specific submatrix inside of
# whole Sudoku matrix.
###############################################################################
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
	#endif

	if (curs_y in range(0, 3)):
		lim_min_y = 0
		lim_max_y = 3

	elif (curs_y in range(3, 6)):
		lim_min_y = 3
		lim_max_y = 6

	elif (curs_y in range(6, 9)):
		lim_min_y = 6
		lim_max_y = 9
	#endif

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
	#endif

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
		matrix[curs_x][curs_y]['solved'] = False
		matrix[curs_x][curs_y]['available_numbers'] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		matrix[curs_x][curs_y]['solution'] = EMPTY
	#endif

	return matrix
#enddef


###############################################################################
# Verify that on particular line there are placed all numbers from 1 to 9.
###############################################################################
def verify_line(matrix, line):
	numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	for i in range(MATRIX_DIM_X):
		if matrix[i][line]['solution'] in numbers:
			numbers.remove(matrix[i][line]['solution'])
		#endif
	#endfor

	if (0 == len(numbers)):
		return True
	else:
		return False
	#endif
#enddef


###############################################################################
# Verify that in particular column there are placed all numbers from 1 to 9.
###############################################################################
def verify_column(matrix, column):
	numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	for i in range(MATRIX_DIM_Y):
		if matrix[column][i]['solution'] in numbers:
			numbers.remove(matrix[column][i]['solution'])
		#endif
	#endfor

	if (0 == len(numbers)):
		return True
	else:
		return False
	#endif
#enddef


###############################################################################
# Verify that in particular submatrix there are placed all numbers from 1 to 9.
###############################################################################
def verify_submatrix(matrix, curs_x, curs_y):
	lim_min_x, lim_max_x, lim_min_y, lim_max_y = find_submatrix_limits(curs_x, curs_y)

	numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	for y in range(lim_min_y, lim_max_y):
		for x in range(lim_min_x, lim_max_x):
			if matrix[x][y]['solution'] in numbers:
				numbers.remove(matrix[x][y]['solution'])
			#endif
		#endfor
	#endfor

	if (0 == len(numbers)):
		return True
	else:
		return False
	#endif
#enddef


###############################################################################
# Go through all lines, columns and submatrices and check that whole Sudoku 
# matrix is filled correctly.
###############################################################################
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


###############################################################################
# Check that whole Sudoku matrix is already filled. This function does not 
# check correctness of the matrix.
###############################################################################
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


###############################################################################
# For already solved element remove its already known number ("solution") from
# all elements which are placed on the same line, column and submatrix.
###############################################################################
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


###############################################################################
# Go through whole matrix and find first element with the lowest count 
# of available numbers.
###############################################################################
def find_unsolved_element(matrix):
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
# Recurrently solve the matrix. Find first unsolved element (with the lowest
# number of possible solutions) and call the solve function again for each
# of these possible solutions.
###############################################################################
def matrix_solve_recurrently(matrix, x, y, number_to_try):
	global gStep
	global gMatrix
	global gMessage

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
			gMessage = "Sudoku is solved!!"
			gMatrix = copy.deepcopy(temp_matrix)
			return True
		else:
			gMessage = "Whole matrix is filled with numbers but it does not pass the checks. We have incorrect solution."
			return False
		#endif
	#endif

	if (False == is_matrix_filled(temp_matrix)):
		gMessage = "Solving ..."
		x, y, available_numbers = find_unsolved_element(temp_matrix)
		refresh_screen(temp_matrix, 0, 0)
		for i in range(len(available_numbers)):
			if (True == matrix_solve_recurrently(temp_matrix, x, y, available_numbers[i])):
				return True
			#endif
		#endfor
	#endif
#enddef


###############################################################################
# Solve the Sudoku matrix.
###############################################################################
def matrix_solve():
	global gMatrix
	global gMessage

	remove_known_numbers(gMatrix)

	if (True == is_matrix_filled(gMatrix)):
		if (True == is_matrix_solved(gMatrix)):
			gMessage = "Sudoku is solved!! No recursion needed."
			return True
		else:
			gMessage = "Whole matrix is filled with numbers but it does not pass the checks. We have incorrect solution."
			return False
		#endif
	#endif

	if (False == is_matrix_filled(gMatrix)):
		x, y, available_numbers = find_unsolved_element(gMatrix)
		for i in range(len(available_numbers)):
			if (True == matrix_solve_recurrently(gMatrix, x, y, available_numbers[i])):
				break
			#endif
		#endfor
	#endif
#enddef


###############################################################################
# Main while loop.
###############################################################################
def main():
	global gMatrix
	global gStep
	global gMessage

	cursor("off")
	os.system('')
	curs_x = 0
	curs_y = 0
	matrix_init(gMatrix)

	g = "0"
	while (ord(g) != BTN_ESC):
		refresh_screen(gMatrix, curs_x, curs_y)
		g = msvcrt.getch()

		if (BTN_UP == ord(g)):
			curs_y = curs_y - 1
			if (curs_y < 0):
				curs_y = 8
			#endif
		#endif

		if (BTN_DOWN == ord(g)):
			curs_y = curs_y + 1
			if (curs_y > 8):
				curs_y = 0
			#endif
		#endif

		if (BTN_RIGHT == ord(g)):
			curs_x = curs_x + 1
			if (curs_x > 8):
				curs_x = 0
			#endif
		#endif

		if (BTN_LEFT == ord(g)):
			curs_x = curs_x - 1
			if (curs_x < 0):
				curs_x = 8
			#endif
		#endif

		if ((ord(g) - ord('0')) in [1, 2, 3, 4, 5, 6, 7, 8, 9]):
			gMatrix = add_value(gMatrix, curs_x, curs_y, int(g))
		#endif

		if (BTN_DELETE == ord(g)):
			gMatrix = delete_value(gMatrix, curs_x, curs_y)
		#endif

		if (BTN_F1 == ord(g)):
			matrix_init(gMatrix)
			curs_x = 0
			curs_y = 0
			gStep = 0
			gMessage = ""
		#endif

		if (BTN_F5 == ord(g)):
			matrix_save_load_menu(gMatrix, "Save")
		#endif

		if (BTN_F6 == ord(g)):
			gMatrix = matrix_save_load_menu(gMatrix, "Load")
			curs_x = 0
			curs_y = 0
			gStep = 0
			gMessage = ""
		#endif

		if (BTN_SPACE == ord(g)):
			gStep = 0
			matrix_solve()
		#endif
	#endwhile

	cursor("on")
#enddef


main()


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
