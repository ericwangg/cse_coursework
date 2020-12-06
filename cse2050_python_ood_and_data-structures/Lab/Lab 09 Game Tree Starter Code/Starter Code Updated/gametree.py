# Here is the board class; it has two attributes, knight and pawns; each piece is a pair of numbers between 0 and 7
class Board:
	def __init__(self, pieces):
		self.knight = pieces[0]
		self.pawns = pieces[1:]

	# prints board as 8 strings, 1 per line, with optional heading
	def printBoard(self, heading=""):
		if (heading):
			print(heading)
		board = [" - - - - - - - -"]*8
		(x,y) = self.knight
		row = board[x]
		board[x] = row[0:2*y+1] + "X" + row[2*y+2:]
		for (x,y) in self.pawns:
			row = board[x]
			board[x] = row[0:2*y+1] + "o" + row[2*y+2:]
		for row in board[:]:
			print(row)

	# returns list of knight moves that will eat a pawn, if any
	def findGoodMoves(self):
		(x0, y0) = self.knight
		moves = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
		goodMoves = []
		for (x, y) in moves:
			(x1, y1) = (x0 + x, y0 + y)
			#print ("trying move ", x, y)
			if (x1, y1) in self.pawns:
				goodMoves += [(x, y)]
		return goodMoves

	# returns a new board that's a copy of this one
	def copyBoard(self):
		newBoard = Board([self.knight]+self.pawns)
		return newBoard

	#given a board and a move, compute the next board
	def applyMove(self, move):
		(x0, y0) = self.knight
		(x, y) = move
		if ((x0 + x) >= 0 and (y0 + y) >= 0) and ((x0 + x) < 8 and (y0 + y) < 8):
			self.knight = (x0 + x, y0 + y)
			if self.knight in self.pawns:
				self.pawns.remove(self.knight)
			return True
		else:
			return False

	## Part 1
	def printGoodMovesBoard(self):
		GoodMoves = self.findGoodMoves()
		for move in GoodMoves:
			newBoard = self.copyBoard()
			newBoard.applyMove(move)
			thisBoard = "Board with move " + str(newBoard.knight)
			newBoard.printBoard(thisBoard)

	def printAllMovesBoard(self):
		moves = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
		for move in moves:
			newBoard = self.copyBoard()
			if newBoard.applyMove(move) == False:
				(x, y) = (move[0] + newBoard.knight[0], move[1] + newBoard.knight[1])
				print("Invalid move: " + str((x,y)))
			else:
				newBoard.printBoard("\nBoard with move " + str(newBoard.knight))

## Part 2
def dfsCapture(board):
	if len(board.pawns) == 0:
		return True
	NiceMoves = board.findGoodMoves()
	sum = 0
	while sum < len(NiceMoves):
		if board.applyMove(NiceMoves[sum]) == True:
			sum += 1
			if sum == len(NiceMoves) - 1:
				return True
		return False

def bfsCapture(board):
	NiceMoves = board.findGoodMoves()
	for move in NiceMoves:
		if len(board.pawns) == 0:
			return True
		elif board.applyMove(move) == True:
			return True
		return False

## Part 3
def findPath(board, path = []):
	if path == []:
		path = [board.knight]
	GoodMoves = board.findGoodMoves()
	if len(board.pawns) == 0:
		GoodMoves = None
		return path
	elif GoodMoves != []:
		for move in GoodMoves:
			board.applyMove(move)
			path.append(board.knight)
			GoodMoves = None
			return findPath(board, path)
	else:
		GoodMoves = None
		return []

# 3 cases, 0 pawns, there are some GoodMoves *s.t. != [], and no GoodMoves

## Part 4
def findAllPaths(board, path=[], paths = None):
	if paths == None:
		paths = []
	if path == []:
		path = [board.knight]
	GoodMoves = board.findGoodMoves()
	if len(board.pawns) == 0:
		GoodMoves = None
		paths.append(path)
		path = None
	elif GoodMoves != []:
		for move in GoodMoves:
			newBoard = board.copyBoard()
			newBoard.applyMove(move)
			newPath = path + [newBoard.knight]
			findAllPaths(newBoard, newPath, paths)
		return paths
	else:
		GoodMoves = None
		newPaths = paths
		paths = []
		return newPaths


# bb = Board([(1,1), (3,2), (5,3), (0,3)])
# bb.printBoard("New board")
# bb.printGoodMovesBoard()
# print('break')
# bb.printAllMovesBoard()

# bb = Board([(1, 1), (0, 3), (1, 5), (2, 3)])
# print(findPath(bb)) ## prints [(2, 3), (1, 5), (0, 3)]

# bb = Board([(1, 1), (0, 3), (1, 5), (2, 3)])
# print(findAllPaths(bb))
## prints [[(1, 1), (2, 3), (1, 5), (0, 3)], [(1, 1), (0, 3), (1, 5), (2, 3)]]
