#########################################################################
# This function returns J and K inputs of a JK flip-flop based on present
# and next state of a state machine.
# 
# 0 -> 0:	0 -> 1:		1 -> 0:		1 -> 1:
#	J = 0		J = 1		J = X		J = X
#	K = X		K = X		K = 1		K = 0
# 
#########################################################################
def getJkInput(presentState, nextState):
	if ((0 == presentState) and (0 == nextState)):
		jInput = 0
		kInput = 'X'
	#endif

	if ((0 == presentState) and (1 == nextState)):
		jInput = 1
		kInput = 'X'
	#endif

	if ((1 == presentState) and (0 == nextState)):
		jInput = 'X'
		kInput = 1
	#endif

	if ((1 == presentState) and (1 == nextState)):
		jInput = 'X'
		kInput = 0
	#endif

	return (jInput, kInput)
#enddef


#########################################################################
# This function initializes a state table which holds all of the states
# (present and next) of a sequential logic circuit. The states are stored 
# in decadic form.
#########################################################################
def initStateTableDec(numOfStates, numOfInputs):
	stateTableDec = []
	numOfCombinations = 2 ** numOfStates

	for i in range(numOfCombinations):
		# Create empty lines.
		stateTableDec.append([])

		# Fill first column (present state combinations).
		stateTableDec[i].append(i)

		# Zero number of inputs is valid value (a circuit has only internal states).
		if (0 == numOfInputs):
			numOfColumns = 1
		else:
			numOfColumns = numOfInputs * 2

		# Fill rest of the columns with zeros (next state combinations).
		for j in range(numOfColumns):
			stateTableDec[i].append(0)
		#endfor
	#endfor

	return stateTableDec
#enddef


#########################################################################
# This function draws a state table. Example (2 states, 3 inputs):
# 
# ╔═══════════════╤═══════════════════════════════════╗
# ║ PresentState  │ NextState                         ║
# ║               ├─────┬─────┬─────┬─────┬─────┬─────╢
# ║               │ A=0 │ A=1 │ B=0 │ B=1 │ C=0 │ C=1 ║
# ╠═══════════════╪═════╪═════╪═════╪═════╪═════╪═════╣
# ║ 0             │ 00  │ 00  │ 00  │ 00  │ 00  │ 00  ║
# ║ 1             │ 00  │ 00  │ 00  │ 00  │ 00  │ 00  ║
# ║ 2             │ 00  │ 00  │ 00  │ 00  │ 00  │ 00  ║
# ║ 3             │ 00  │ 00  │ 00  │ 00  │ 00  │ 00  ║
# ╚═══════════════╧═════╧═════╧═════╧═════╧═════╧═════╝ 
#########################################################################
def drawStateTableDec(stateTableDec, numOfStates, numOfInputs):
	COLUMN_NAME = "NextState "
	COLUMN_WIDTH = 6

	lineLen = numOfInputs * COLUMN_WIDTH * 2
	lenth = lineLen if (lineLen > len(COLUMN_NAME)) else len(COLUMN_NAME) + 2
	numOfCombinations = 2 ** numOfStates
	numOfLeadingZeros = len(str(numOfCombinations))

	# Draw 1st line of the table.
	print("╔══════════════╤" + ("═" * (lenth - 1))                                   +   "╗")

	# Draw 2nd line of the table.
	print("║ PresentState │ " + COLUMN_NAME + (" " * (lenth - len(COLUMN_NAME) - 2)) +   "║")

	# Draw 3rd line of the table.
	if (0 == numOfInputs):
		print("║              ├───────────╢")
	else:
		print("║              ├" + ("─────┬" * numOfInputs * 2)                      + "\b╢")
	#endif

	# Draw 4th line of the table.
	print("║              ", end = "")
	if (0 == numOfInputs):
		print("│           ", end = "")
	else:
		for i in range(65, 65 + numOfInputs, 1):
			print("│ " + chr(i) + "=0 │ " + chr(i) + "=1 ", end = "")
		#endfor
	#endif
	print("║")

	# Draw 5th line of the table.
	if (0 == numOfInputs):
		print("╠══════════════╪═══════════╣")
	else:
		print("╠══════════════╪" + ("═════╪" * numOfInputs * 2)                      + "\b╣")
	#endif

	# Draw lines 6 to 6 + 2^numOfStates (state combinations).
	for i in range(numOfCombinations):
		if (0 == numOfInputs):
			print("║ " + str(stateTableDec[i][0]).zfill(numOfLeadingZeros) + (" " * (13 - numOfLeadingZeros)) + "│", end = "")
			print(" "  + str(stateTableDec[i][1]).zfill(numOfLeadingZeros) + (" " * (10 - numOfLeadingZeros)) + "║")
		else:
			print("║ " + str(stateTableDec[i][0]).zfill(numOfLeadingZeros) + (" " * (13 - numOfLeadingZeros)) + "│", end = "")

			# Draw next states for each of the inputs.
			for j in range(1, (numOfInputs * 2) + 1, 1):
				print(" "  + str(stateTableDec[i][j]).zfill(numOfLeadingZeros) + (" " *  (4 - numOfLeadingZeros)) + "│", end = "")
			#endfor

			print("\b║")
		#endif
	#endfor

	# Draw the last line of the table.
	if (0 == numOfInputs):
		print("╚══════════════╧═══════════╧"                                         + "\b╝")
	else:
		print("╚══════════════╧" + ("═════╧" * numOfInputs * 2)                      + "\b╝")
	#endif
#enddef


#########################################################################
# This function generates table of present state combinations
# of a sequential logic circuit.
#########################################################################
# def getPresentStateCombinations(numOfStates):
# 	presentStateTable = []
# 	numOfCombinations = 2 ** numOfStates

# 	for i in range(numOfCombinations):
# 		presentStateTable.append([])
# 		binNum = bin(i).replace("0b", "").zfill(numOfStates)

# 		for j in range(numOfStates):
# 			presentStateTable[i].append(binNum[j])
# 		#endfor
# 	#endfor	

# 	return presentStateTable
# #enddef	


# def drawStateTableBin(numOfStates):
# 	COLUMN_NAME_1 = "Present State  "
# 	COLUMN_NAME_2 = "Next State     "
# 	COLUMN_WIDTH = 3
# 	MIN_NUM_OF_COLUMNS = 5

# 	lineLen = numOfStates * COLUMN_WIDTH
# 	strLen = len(COLUMN_NAME_1)
# 	lenth = lineLen if (lineLen > strLen) else strLen
# 	extraSpace1 = (lineLen - strLen) if (lineLen > strLen) else 0
# 	extraSpace2 = (strLen - lineLen) if (lineLen < strLen) else 0
# 	numOfCombinations = 2 ** numOfStates

# 	# Draw 1st line of the table.
# 	print("╔═" + ("═" * lenth)                       + "╤" + ("═" * lenth)                        + "═╗")

# 	# Draw 2nd line of the table.
# 	print("║ " + COLUMN_NAME_1 + (" " * extraSpace1) + "│ " + COLUMN_NAME_2 + (" " * extraSpace1) +  "║")

# 	# Draw 3rd line of the table.
# 	print("╠═" + ("═" * lenth)                       + "╪" + ("═" * lenth)                        + "═╣")

# 	# Draw 4th line of the table.
# 	print("║ ", end = "")
# 	for i in range(numOfStates - 1, -1, -1):
# 		print('Q', i, " ", sep = "", end = "")
# 	#endfor
# 	print((" " * extraSpace2) + "│ ", end = "")
# 	for i in range(numOfStates - 1, -1, -1):
# 		print('Q', i, " ", sep = "", end = "")
# 	#endfor
# 	print((" " * extraSpace2) + "║")

# 	# Draw 5th line of the table.
# 	print("╟─" + ("─" * lenth)                       + "┼" + ("─" * lenth)                        + "─╢")

# 	# Draw state combinations (lines 6 to 6 + 2^numOfStates).
# 	presentStateTable = getPresentStateCombinations(numOfStates)
# 	for i in range(numOfCombinations):
# 		print("║", end = "")
# 		for j in range(numOfStates):
# 			print("  " + presentStateTable[i][j], end = "")
# 		#endfor
# 		print((" " * extraSpace2)                   + " │ " + (" " * lenth)                       +  "║")
# 	#endfor

# 	# Draw the last line of the table.
# 	print("╚═" + ("═" * lenth)                       + "╧" + ("═" * lenth)                        + "═╝")
# #enddef


def main():
	numOfStates = 4
	numOfInputs = 4

	gStateTableDec = initStateTableDec(numOfStates, numOfInputs)
	drawStateTableDec(gStateTableDec, numOfStates, numOfInputs)

	# drawStateTableBin(4)

#enddef


main()

# Change to class:
# class Table
# 	attribute stateTableDec
# 	method initStateTableDec
# 	method drawStateTableDec
# 	method saveTable
# 	method loadTable

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