import random

def sudokuGen():
	""" Returns a Sudoku board """

	board = [[cell() for _ in range(9)] for _ in range(9)]
	stack = [board[0][0]] + [None] * 80
	index = 1

	while index < 81:
		if not stack[index]:
			stack[index] = board[index // 9][index % 9]
		else:
			stack[index].index += 1
			if stack[index].index == 9:
				stack[index].index = 0
				stack[index] = None
				index -= 1
				continue

		if test_cell([stack[9 * i : 9 * i + 9] for i in range(9)], 
					(index // 9, index % 9)):
			index += 1

	return board

def solve(puzzle):
	""" Returns:
	Completed Sudoku puzzle -- if the puzzle is solvable
	None -- if the puzzle is not solvable """

	def solver(sudoku, queue):
		if not queue:
			return sudoku
		queue.sort(key = lambda x: len(x[1]))
		currCell = queue.pop(0)
		if len(currCell[1]) == 0:
			return None
		x, y = currCell[0]
		sudoku[x][y] = cell(False)
		for sudoku[x][y].index in currCell[1]:
			tempQueue = []
			for c in queue:
				emptyCell = (c[0], list(c[1]))
				if sudoku[x][y].index in emptyCell[1]:
					x1, y1 = emptyCell[0]
					if x == x1 or y == y1:
						emptyCell[1].remove(sudoku[x][y].index)
					elif x // 3 == x1 // 3 and y // 3 == y1 // 3:
						emptyCell[1].remove(sudoku[x][y].index)
				if len(emptyCell[1]) == 0:
					break
				tempQueue.append(emptyCell)
			else:	# No break
				solution = solver(copy(sudoku), tempQueue)
				if solution:
					return solution
	
	q = []
	for x in range(9):
		for y in range(9):
			if not puzzle[x][y]:
				q.append(((x, y), possibilities(puzzle, x, y)))
	
	return solver(copy(puzzle), q)

def puzzleGen(board):
	""" Creates a puzzle from a completed Sudoku board """

	puzzle = copy(board)
	cells = [num for num in range(81)]
	random.shuffle(cells)

	for index in cells:
		x, y = index // 9, index % 9
		cell_backup = puzzle[x][y]
		puzzle[x][y] = cell(False)
		for puzzle[x][y].index in range(9):
			if puzzle[x][y].value == cell_backup.value:
				continue
			if test_cell(puzzle, (x, y)) and solve(puzzle):
				puzzle[x][y] = cell_backup
				break
		else:	# No break
			puzzle[x][y] = None

	return puzzle

def test_cell(board, position):
	""" Checks if the cell's value in the given coordinates is valid """

	x, y = position
	for i in range(9):
		# Tests column
		if i != x and board[i][y] and board[i][y].value == board[x][y].value:
			return False
		# Tests row
		if i != y and board[x][i] and board[x][i].value == board[x][y].value:
			return False
	
	# Tests box
	for i in range((x // 3) * 3, (x // 3) * 3 + 3):
		for j in range((y // 3) * 3, (y // 3) * 3 + 3):
			if i == x and j == y:
				continue
			if board[i][j] and board[i][j].value == board[x][y].value:
				return False

	return True

def possibilities(puzzle, x, y):
	""" Returns a list of possibilities for the cell in coordinates x, y """

	retList = [i for i in range(9)]
	cell_backup = puzzle[x][y]
	puzzle[x][y] = cell(False)
	for puzzle[x][y].index in range(9):
		if not test_cell(puzzle, (x, y)):
			retList.remove(puzzle[x][y].index)
	puzzle[x][y] = cell_backup
	return retList

def copy(board):
	""" Returns a deep copy of a board """

	temp = [[None for _ in range(9)] for _ in range(9)]
	for x in range(9):
		for y in range(9):
			if board[x][y]:
				temp[x][y] = cell(False)
				temp[x][y].index = board[x][y].value - 1
	return temp

def print_board(board):
	""" Prints the given board """
	
	print('-' * 25)
	for i in range(9):
		line = []
		for x in range(9):
			if board[i][x]:
				line.append(board[i][x].value)
			else:
				line.append(0)
		print('| {} {} {} | {} {} {} | {} {} {} |'.format(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8]))
		if (i + 1) % 3 == 0:
			print('-' * 25)

class cell:
	def __init__(self, rand = True):
		self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		self.index = 0

		if rand:
			random.shuffle(self.numbers)

	@property
	def value(self):
		return self.numbers[self.index]
